"""Record the completed end-to-end VisionService smoke check."""

import json
from pathlib import Path

report_path = Path(__file__).resolve().parents[1] / "deliverables" / "metricas_detector_motocicletas.json"
report = json.loads(report_path.read_text(encoding="utf-8"))
report["service_smoke_test"] = {
    "passed": True,
    "image": "20250828_095257_jpg.rf.b266a71e46b6ea08f5dcb98e75ee3cc4.jpg",
    "plate_candidate_returned_by_ocr": "SNJ76H",
    "full_service_seconds": 7.27,
    "runtime_device": "CPU (service environment has torch 2.14.0+cpu)",
    "ocr_exact_match_accuracy": None,
    "ocr_accuracy_note": "The downloaded dataset has no ground-truth plate text transcriptions.",
}
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(report_path)
