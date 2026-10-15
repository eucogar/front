"""Re-evaluate the deployed motorcycle plate detector on held-out test data."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime
from pathlib import Path


FRONT_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = FRONT_DIR.parent
VISION_DIR = PROJECT_DIR / "VisionArtificial"
WORK_DIR = FRONT_DIR / ".codex-vision-work"
DATASET_DIR = VISION_DIR / "img" / "DetectionColombianMotoPlates.v15-v5.0_yolo12accurate_672strfillcentercropin.yolov8"
DATA_YAML = WORK_DIR / "dataset.yaml"
MODEL_PATH = VISION_DIR / "plate_detector.pt"
OUTPUT_PATH = FRONT_DIR / "deliverables" / "test_modelo_vision_20261012.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    if not MODEL_PATH.is_file() or not DATA_YAML.is_file():
        raise SystemExit(f"Falta el modelo o el YAML del dataset: {MODEL_PATH} / {DATA_YAML}")

    sys.dont_write_bytecode = True
    sys.path.insert(0, str(WORK_DIR / "cuda-site"))
    sys.path.insert(1, str(VISION_DIR / ".venv" / "Lib" / "site-packages"))
    os.environ["YOLO_CONFIG_DIR"] = str(WORK_DIR / "api-settings")

    import torch
    import ultralytics
    from ultralytics import YOLO

    if not torch.cuda.is_available():
        raise SystemExit("CUDA no está disponible; no se ejecutó una evaluación lenta en CPU.")

    print(f"Modelo: {MODEL_PATH}", flush=True)
    print(f"Dataset de prueba: {DATASET_DIR / 'test' / 'images'}", flush=True)
    print(f"GPU: {torch.cuda.get_device_name(0)}", flush=True)

    model = YOLO(str(MODEL_PATH))
    started = time.perf_counter()
    result = model.val(
        data=str(DATA_YAML),
        split="test",
        imgsz=640,
        batch=16,
        device="0",
        workers=0,
        plots=False,
        project=str(FRONT_DIR / "deliverables" / "evaluacion_modelo_vision"),
        name="test_20261012",
        exist_ok=True,
        verbose=False,
    )
    elapsed = time.perf_counter() - started
    box = result.box
    test_images = list((DATASET_DIR / "test" / "images").glob("*"))
    report = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "scope": "Evaluación del detector de cajas de placa sobre el split test reservado.",
        "dataset": DATASET_DIR.name,
        "split": "test",
        "images": len(test_images),
        "model": str(MODEL_PATH),
        "model_sha256": sha256(MODEL_PATH),
        "environment": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "ultralytics": ultralytics.__version__,
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
        },
        "parameters": {"image_size": 640, "batch": 16, "confidence_threshold": 0.001, "iou_threshold": 0.7},
        "metrics": {
            "precision": round(float(box.mp), 6),
            "recall": round(float(box.mr), 6),
            "map50": round(float(box.map50), 6),
            "map50_95": round(float(box.map), 6),
            "speed_ms_per_image": {key: round(float(value), 3) for key, value in result.speed.items()},
            "evaluation_seconds": round(elapsed, 2),
        },
        "limitations": [
            "Precisión, recall y mAP miden la localización de la placa, no la transcripción OCR exacta.",
            "El dataset no tiene transcripciones de texto para todas las placas, así que no permite calcular exactitud OCR general.",
            "El resultado corresponde al split test de 101 imágenes; no prueba generalización a todas las cámaras del campus.",
        ],
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("MÉTRICAS:", json.dumps(report["metrics"], ensure_ascii=False), flush=True)
    print("IMÁGENES:", len(test_images), flush=True)
    print("REPORTE:", OUTPUT_PATH, flush=True)


if __name__ == "__main__":
    main()
