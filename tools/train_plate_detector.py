"""Train and evaluate a plate detector on the downloaded Colombian motorcycle dataset.

Run from the front project with the VisionArtificial Python dependencies:
    py -3.14 tools/train_plate_detector.py

The Roboflow test split is held out during training and used only for the
baseline/final comparison. Polygon annotations are converted by Ultralytics to
axis-aligned boxes because this project uses object detection, not segmentation.
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path


FRONT_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = FRONT_DIR.parent
VISION_DIR = PROJECT_DIR / "VisionArtificial"
DATASET_DIR = VISION_DIR / "img" / "DetectionColombianMotoPlates.v15-v5.0_yolo12accurate_672strfillcentercropin.yolov8"
BASE_WEIGHTS = VISION_DIR / "yolov8n.pt"
WORK_DIR = FRONT_DIR / ".codex-vision-work"
CUDA_SITE = WORK_DIR / "cuda-site"
RUN_DIR = WORK_DIR / "runs"
TRAIN_RUN = RUN_DIR / "plates_yolov8n_cuda"
DATA_YAML = WORK_DIR / "dataset.yaml"
FINAL_WEIGHTS = FRONT_DIR / "deliverables" / "plate_detector_yolov8n.pt"
REPORT_PATH = FRONT_DIR / "deliverables" / "metricas_detector_motocicletas.json"


def collect_metrics(results) -> dict[str, object]:
    box = results.box
    return {
        "precision": round(float(box.mp), 6),
        "recall": round(float(box.mr), 6),
        "map50": round(float(box.map50), 6),
        "map50_95": round(float(box.map), 6),
        "speed_ms_per_image": {key: round(float(value), 3) for key, value in results.speed.items()},
    }


def main() -> None:
    if not DATASET_DIR.is_dir() or not BASE_WEIGHTS.is_file():
        raise SystemExit(f"Falta el dataset o el modelo base: {DATASET_DIR} / {BASE_WEIGHTS}")
    for split in ("train", "valid", "test"):
        if not (DATASET_DIR / split / "images").is_dir() or not (DATASET_DIR / split / "labels").is_dir():
            raise SystemExit(f"El split {split} no tiene images/ y labels/.")
    site_packages = VISION_DIR / ".venv" / "Lib" / "site-packages"
    if not site_packages.is_dir():
        raise SystemExit(f"No existe el entorno de dependencias esperado: {site_packages}")

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    (FRONT_DIR / "deliverables").mkdir(parents=True, exist_ok=True)
    DATA_YAML.write_text(
        "path: " + DATASET_DIR.as_posix() + "\n"
        "train: train/images\n"
        "val: valid/images\n"
        "test: test/images\n"
        "names:\n  0: plates\n",
        encoding="utf-8",
    )

    sys.dont_write_bytecode = True
    if CUDA_SITE.is_dir():
        sys.path.insert(0, str(CUDA_SITE))
    sys.path.insert(1 if CUDA_SITE.is_dir() else 0, str(site_packages))

    # Keep Ultralytics-generated settings and run artifacts inside the writable front project.
    with tempfile.TemporaryDirectory(prefix=".yolo-config-", dir=WORK_DIR) as config_dir:
        os.environ["YOLO_CONFIG_DIR"] = config_dir
        import ultralytics
        from ultralytics import YOLO
        import torch
        ultralytics_version = ultralytics.__version__

        if not torch.cuda.is_available():
            raise SystemExit("El entorno CUDA no reconoce la GPU; no se iniciará un entrenamiento lento en CPU.")
        device = "0"
        print(f"CUDA device: {torch.cuda.get_device_name(0)}", flush=True)
        print("Evaluating the original COCO-pretrained detector on held-out test split...", flush=True)
        baseline_model = YOLO(str(BASE_WEIGHTS))
        baseline_started = time.perf_counter()
        baseline_result = baseline_model.val(
            data=str(DATA_YAML), split="test", imgsz=640, batch=16, device=device,
            workers=0, plots=False, project=str(RUN_DIR), name="baseline_test", exist_ok=True,
            verbose=False,
        )
        baseline_seconds = time.perf_counter() - baseline_started
        baseline_metrics = collect_metrics(baseline_result)
        print(f"Baseline on test: {baseline_metrics}", flush=True)

        print("Training YOLOv8n: 50 epochs max, early stopping patience 10, image size 640, RTX 3060...", flush=True)
        train_started = time.perf_counter()
        trained_model = YOLO(str(BASE_WEIGHTS))
        trained_model.train(
            data=str(DATA_YAML),
            task="detect",
            epochs=50,
            patience=10,
            imgsz=640,
            batch=16,
            device=device,
            amp=False,
            workers=0,
            seed=42,
            deterministic=True,
            cache=False,
            plots=False,
            project=str(RUN_DIR),
            name="plates_yolov8n_cuda",
            exist_ok=True,
            verbose=False,
            close_mosaic=10,
        )
        training_seconds = time.perf_counter() - train_started
        best_weights = TRAIN_RUN / "weights" / "best.pt"
        if not best_weights.is_file():
            raise SystemExit(f"No apareció el peso entrenado esperado: {best_weights}")

        print("Evaluating the trained detector on the same untouched test split...", flush=True)
        final_model = YOLO(str(best_weights))
        final_started = time.perf_counter()
        final_result = final_model.val(
            data=str(DATA_YAML), split="test", imgsz=640, batch=16, device=device,
            workers=0, plots=False, project=str(RUN_DIR), name="trained_test", exist_ok=True,
            verbose=False,
        )
        final_seconds = time.perf_counter() - final_started
        final_metrics = collect_metrics(final_result)

    shutil.copy2(best_weights, FINAL_WEIGHTS)
    split_counts = {}
    for split in ("train", "valid", "test"):
        images = list((DATASET_DIR / split / "images").glob("*"))
        labels = list((DATASET_DIR / split / "labels").glob("*.txt"))
        split_counts[split] = {"images": len(images), "label_files": len(labels)}

    report = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "dataset": {
            "name": DATASET_DIR.name,
            "source": "https://universe.roboflow.com/itm-n1i3r/detectioncolombianmotoplates-6o1aj/dataset/15",
            "license": "CC BY 4.0",
            "split_counts": split_counts,
            "annotations": "YOLO polygon labels converted to axis-aligned plate boxes by Ultralytics for detection.",
            "test_split_used_only_for_evaluation": True,
        },
        "environment": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "ultralytics": ultralytics_version,
            "torch": torch.__version__,
            "device": f"CUDA: {torch.cuda.get_device_name(0)}",
            "initial_weights": str(BASE_WEIGHTS),
        },
        "training": {
            "base_model": "YOLOv8n COCO checkpoint",
            "task": "plate object detection",
            "epochs_max": 50,
            "early_stopping_patience": 10,
            "image_size": 640,
            "batch": 16,
            "seed": 42,
            "training_seconds": round(training_seconds, 2),
            "best_weights": str(FINAL_WEIGHTS),
        },
        "test_metrics_baseline": {**baseline_metrics, "evaluation_seconds": round(baseline_seconds, 2)},
        "test_metrics_trained": {**final_metrics, "evaluation_seconds": round(final_seconds, 2)},
        "limitations": [
            "These metrics score plate bounding-box detection, not exact character transcription by OCR.",
            "The downloaded images may not be independent vehicles or match UPC camera conditions; this must be checked before claiming campus generalization.",
            "The OCR labels are not included as text transcriptions, so exact plate-reading accuracy cannot be calculated from this dataset alone.",
        ],
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Trained detector test metrics: {final_metrics}", flush=True)
    print(f"Training seconds: {training_seconds:.2f}; best checkpoint: {FINAL_WEIGHTS}", flush=True)
    print(f"Report: {REPORT_PATH}", flush=True)


if __name__ == "__main__":
    main()
