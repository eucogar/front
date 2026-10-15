"""Evaluate existing training output on held-out test data and publish artifacts."""

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

from train_plate_detector import (
    BASE_WEIGHTS, DATASET_DIR, FINAL_WEIGHTS, FRONT_DIR, REPORT_PATH,
    RUN_DIR, VISION_DIR, WORK_DIR, collect_metrics,
)


def main() -> None:
    site_packages = VISION_DIR / ".venv" / "Lib" / "site-packages"
    cuda_site = WORK_DIR / "cuda-site"
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(site_packages))
    sys.path.insert(0, str(cuda_site))
    best = RUN_DIR / "plates_yolov8n" / "weights" / "best.pt"
    if not best.is_file():
        raise SystemExit(f"No existe el modelo entrenado: {best}")

    with tempfile.TemporaryDirectory(prefix=".yolo-final-config-", dir=WORK_DIR) as config_dir:
        os.environ["YOLO_CONFIG_DIR"] = config_dir
        import torch
        import ultralytics
        from ultralytics import YOLO

        if not torch.cuda.is_available():
            raise SystemExit("CUDA no disponible para la evaluación")
        device = "0"
        data_yaml = WORK_DIR / "dataset.yaml"
        print(f"Evaluando en GPU: {torch.cuda.get_device_name(0)}", flush=True)
        started = time.perf_counter()
        baseline = YOLO(str(BASE_WEIGHTS)).val(
            data=str(data_yaml), split="test", imgsz=640, batch=16,
            device=device, workers=0, plots=False, project=str(RUN_DIR),
            name="baseline_test_final", exist_ok=True, verbose=False,
        )
        baseline_seconds = time.perf_counter() - started

        started = time.perf_counter()
        trained = YOLO(str(best)).val(
            data=str(data_yaml), split="test", imgsz=640, batch=16,
            device=device, workers=0, plots=False, project=str(RUN_DIR),
            name="trained_test_final", exist_ok=True, verbose=False,
        )
        trained_seconds = time.perf_counter() - started

    shutil.copy2(best, FINAL_WEIGHTS)
    from train_plate_detector import collect_metrics

    split_counts = {}
    for split in ("train", "valid", "test"):
        split_counts[split] = {
            "images": len(list((DATASET_DIR / split / "images").glob("*"))),
            "label_files": len(list((DATASET_DIR / split / "labels").glob("*.txt"))),
        }
    report = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "dataset": {
            "name": DATASET_DIR.name,
            "source": "https://universe.roboflow.com/itm-n1i3r/detectioncolombianmotoplates-6o1aj/dataset/15",
            "license": "CC BY 4.0",
            "split_counts": split_counts,
            "annotations": "YOLO polygons converted to axis-aligned plate boxes for object detection.",
            "test_split_used_only_for_evaluation": True,
        },
        "environment": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "ultralytics": ultralytics.__version__,
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
        },
        "training": {
            "base_model": "YOLOv8n pretrained on COCO",
            "task": "motorcycle plate object detection",
            "epochs_completed": 50,
            "image_size": 640,
            "batch": 16,
            "seed": 42,
            "best_weights": str(FINAL_WEIGHTS),
        },
        "test_metrics_baseline": {**collect_metrics(baseline), "evaluation_seconds": round(baseline_seconds, 2)},
        "test_metrics_trained": {**collect_metrics(trained), "evaluation_seconds": round(trained_seconds, 2)},
        "limitations": [
            "These are plate-box detection metrics, not exact OCR transcription accuracy.",
            "The dataset does not include ground-truth plate text transcriptions.",
            "Campus camera conditions and independence of vehicles/images must be confirmed before generalizing.",
            "Small dataset: 300 training images, 100 validation images, 101 test images.",
        ],
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("TEST BASELINE:", json.dumps(collect_metrics(baseline)), flush=True)
    print("TEST TRAINED:", json.dumps(collect_metrics(trained)), flush=True)
    print("WEIGHTS:", FINAL_WEIGHTS, FINAL_WEIGHTS.stat().st_size, "bytes", flush=True)
    print("REPORT:", REPORT_PATH, flush=True)


if __name__ == "__main__":
    main()
