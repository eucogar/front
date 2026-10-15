"""Benchmark the current UPC plate recognizer on the labeled local pilot set.

Run from the front project with Python 3.14 available and the VisionArtificial
virtualenv packages present:
    py -3.14 tools/vision_benchmark.py

The two labels are manually transcribed from the supplied original photographs.
Repeated runs are for latency/consistency only; they are not independent images.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import statistics
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path


FRONT_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = FRONT_DIR.parent
VISION_DIR = PROJECT_DIR / "VisionArtificial"
SITE_PACKAGES = VISION_DIR / ".venv" / "Lib" / "site-packages"
LABELS_FILE = Path(__file__).with_name("vision_test_labels.csv")
OUTPUT_FILE = FRONT_DIR / "deliverables" / "metricas_vision_piloto.json"
REPETITIONS = 5


def percentile(values: list[float], percentage: float) -> float:
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, round((len(ordered) - 1) * percentage)))
    return ordered[index]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    if not SITE_PACKAGES.is_dir():
        raise SystemExit(f"No existe el entorno de dependencias esperado: {SITE_PACKAGES}")

    sys.dont_write_bytecode = True
    sys.path.insert(0, str(SITE_PACKAGES))
    sys.path.insert(0, str(VISION_DIR))

    # Keep Ultralytics' generated settings inside a temporary directory in the
    # writable front workspace. EasyOCR uses its already populated local cache.
    with tempfile.TemporaryDirectory(prefix=".vision-bench-", dir=FRONT_DIR) as config_dir:
        os.environ["YOLO_CONFIG_DIR"] = config_dir
        os.environ.setdefault("EASYOCR_MODULE_PATH", str(Path.home() / ".EasyOCR"))

        import cv2
        import easyocr
        import torch
        import ultralytics
        from vision_service import VisionService

        cases: list[tuple[str, str]] = []
        with LABELS_FILE.open(newline="", encoding="utf-8-sig") as file:
            for row in csv.DictReader(file):
                cases.append((row["filename"], row["expected_plate"].strip().upper()))
        if not cases:
            raise SystemExit("El CSV no contiene imágenes etiquetadas.")

        model_path = VISION_DIR / "yolov8n.pt"
        started = time.perf_counter()
        service = VisionService(model_path=str(model_path))
        model_load_seconds = time.perf_counter() - started

        # One warm-up call per image is excluded from latency measurements.
        for filename, _ in cases:
            service.procesar_archivo(str(VISION_DIR / "img" / filename))

        observations: list[dict[str, object]] = []
        latencies: list[float] = []
        for filename, expected in cases:
            for repetition in range(1, REPETITIONS + 1):
                image_path = VISION_DIR / "img" / filename
                started = time.perf_counter()
                predicted = service.procesar_archivo(str(image_path))
                elapsed = time.perf_counter() - started
                latencies.append(elapsed)
                observations.append(
                    {
                        "filename": filename,
                        "repetition": repetition,
                        "expected": expected,
                        "predicted": predicted or None,
                        "exact_match": predicted == expected,
                        "latency_seconds": round(elapsed, 4),
                    }
                )

        # Score each unique photograph once, using its first measured prediction.
        first_by_image: dict[str, dict[str, object]] = {}
        for observation in observations:
            first_by_image.setdefault(str(observation["filename"]), observation)
        correct_unique = sum(bool(item["exact_match"]) for item in first_by_image.values())
        correct_runs = sum(bool(item["exact_match"]) for item in observations)

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "scope": "Prueba piloto local del servicio de visión; no evalúa el back ni condiciones de campus.",
            "ground_truth": "Placas transcritas manualmente de las fotografías originales; no es una muestra independiente grande.",
            "environment": {
                "os": platform.platform(),
                "python": platform.python_version(),
                "opencv": cv2.__version__,
                "easyocr": easyocr.__version__,
                "ultralytics": ultralytics.__version__,
                "torch": torch.__version__,
                "device": "CPU" if not torch.cuda.is_available() else "CUDA",
                "model": str(model_path),
                "model_sha256": sha256(model_path),
            },
            "method": {
                "unique_images": len(cases),
                "repetitions_per_image_for_latency": REPETITIONS,
                "warmup_per_image_excluded_from_latency": 1,
                "model_initialization_seconds_excluded_from_image_latency": round(model_load_seconds, 4),
                "score_rule": "Coincidencia exacta de los 6 caracteres; distingue posición y carácter.",
            },
            "metrics": {
                "unique_image_exact_accuracy_numerator": correct_unique,
                "unique_image_exact_accuracy_denominator": len(cases),
                "unique_image_exact_accuracy_percent": round(100 * correct_unique / len(cases), 2),
                "repeated_run_exact_matches": correct_runs,
                "repeated_run_count": len(observations),
                "repeated_run_exact_match_percent_not_independent": round(100 * correct_runs / len(observations), 2),
                "latency_ms_mean": round(1000 * statistics.mean(latencies), 2),
                "latency_ms_median": round(1000 * statistics.median(latencies), 2),
                "latency_ms_p95_nearest_rank": round(1000 * percentile(latencies, 0.95), 2),
            },
            "observations": observations,
            "limitations": [
                "Solo se usaron dos imágenes distintas, ambas locales; los reintentos no aumentan el tamaño de la muestra.",
                "La referencia fue transcrita manualmente y no representa una validación independiente en campus.",
                "No se midieron precisión/recall de detección de objetos, falsos positivos en escenas negativas, carga concurrente, ni tiempos del API o SQL Server.",
            ],
        }
        OUTPUT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        print(f"Reporte: {OUTPUT_FILE}")
        print(f"Imágenes únicas: {len(cases)}; coincidencias exactas: {correct_unique}/{len(cases)} ({report['metrics']['unique_image_exact_accuracy_percent']}%)")
        print(f"Ejecuciones medidas: {len(observations)}; coincidencias: {correct_runs}/{len(observations)}")
        print(f"Latencia media: {report['metrics']['latency_ms_mean']} ms; mediana: {report['metrics']['latency_ms_median']} ms; p95: {report['metrics']['latency_ms_p95_nearest_rank']} ms")
        for item in observations:
            print(f"{item['filename']} #{item['repetition']}: esperado={item['expected']} predicho={item['predicted'] or 'sin lectura'} exacta={item['exact_match']} {item['latency_seconds']} s")


if __name__ == "__main__":
    main()
