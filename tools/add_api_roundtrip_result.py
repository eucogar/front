"""Record the local API smoke check performed against the real FastAPI app."""

import json
from pathlib import Path

report_path = Path(__file__).resolve().parents[1] / "deliverables" / "metricas_detector_motocicletas.json"
report = json.loads(report_path.read_text(encoding="utf-8"))
report["api_end_to_end_test"] = {
    "server": "127.0.0.1:8000 (temporary local run; stopped after check)",
    "health": {"status_code": 200, "response": {"status": "ok"}},
    "detectar": {
        "status_code": 200,
        "request_content_type": "multipart/form-data",
        "file_field": "imagen",
        "response": {"placa": "SNJ76H"},
        "torch_cuda_available": True,
        "device_selection": "Ultralytics automatic device selection",
    },
    "image": "20250828_095257_jpg.rf.b266a71e46b6ea08f5dcb98e75ee3cc4.jpg",
}
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(report_path)
