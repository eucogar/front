from PIL import Image, ImageDraw
from pathlib import Path
src=Path(r'C:\Users\euco\AppData\Local\Temp\codex-clipboard-83b9a1d2-7925-4579-bba4-842ce74a5c6a.jpg')
out=Path(r'C:\Users\euco\Desktop\PROYECTO\front\.codex-doc-preview\captura_registro_segura.jpg')
with Image.open(src) as im:
    w,h=im.size
    # Keep the success banner and empty form only; exclude the ID and OCR result rows.
    crop=im.crop((int(w*.04),int(h*.22),int(w*.97),int(h*.60)))
    # End cleanly after the plate input, removing the next helper-text line.
    ImageDraw.Draw(crop).rectangle((7,456,crop.width-7,crop.height),fill=(15,22,41))
    crop.save(out,quality=92)
print(out, Image.open(out).size)
