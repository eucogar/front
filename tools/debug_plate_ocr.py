import sys
from pathlib import Path
import importlib.util
import cv2

vision_dir = Path(r"C:\Users\euco\Desktop\PROYECTO\VisionArtificial")
sys.path.insert(0, str(vision_dir))
service_path = Path(__file__).resolve().parents[1] / "deliverables" / "vision_service.py"
spec = importlib.util.spec_from_file_location("patched_vision_service", service_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
VisionService = module.VisionService

image_path = Path(r"C:\Users\euco\AppData\Local\Temp\codex-clipboard-6b6e8f92-6ab2-4660-9034-07cc4d892770.jpg")
service = VisionService(str(Path(__file__).resolve().parents[1] / "deliverables" / "plate_detector_yolov8n.pt"))
assert service.limpiar_placa("COLOMBIA") == ""
assert service.limpiar_placa("HXFJ05F") == "HXF05F"
assert service.limpiar_placa("HXF05F") == "HXF05F"
image = cv2.imread(str(image_path))
result = service.model(image, verbose=False)[0]
for det in result.boxes:
    x1, y1, x2, y2 = map(int, det.xyxy[0])
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(image.shape[1], x2), min(image.shape[0], y2)
    region = image[y1:y2, x1:x2]
    escala = min(3.0, max(1.0, 1000 / max(region.shape[:2])))
    grande = cv2.resize(region, None, fx=escala, fy=escala, interpolation=cv2.INTER_CUBIC)
    gris = cv2.cvtColor(grande, cv2.COLOR_BGR2GRAY)
    contraste = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gris)
    variantes = [grande, contraste, cv2.threshold(contraste, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]]
    for i, variante in enumerate(variantes):
        lecturas = service.reader.readtext(variante, detail=1, paragraph=False, allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", decoder="greedy")
        print("variant", i, "shape", variante.shape)
        for bbox, text, confidence in lecturas:
            cy = sum(point[1] for point in bbox) / len(bbox)
            print("ocr", repr(text), round(float(confidence), 3), round(cy / variante.shape[0], 3), "clean", service.limpiar_placa(text))
print("plate_result", service._procesar(image))
