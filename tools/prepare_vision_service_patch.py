"""Create a staged OCR correction from VisionArtificial's VisionService."""

from pathlib import Path

source = Path(__file__).resolve().parents[2] / "VisionArtificial" / "vision_service.py"
target = Path(__file__).resolve().parents[1] / "deliverables" / "vision_service.py"
text = source.read_text(encoding="utf-8")

patches = [
    (
        '''    @staticmethod
    def limpiar_placa(texto: str) -> str:
        limpio = re.sub(r"[^A-Z0-9]", "", texto.upper())
        for inicio in range(max(0, len(limpio) - 5)):
            candidato = limpio[inicio:inicio + 6]
            if len(candidato) != 6 or not re.match(r"^[A-Z]{3}", candidato):
                continue
            candidato = candidato[:3] + candidato[3:5].translate(
                str.maketrans({"O": "0", "Q": "0", "D": "0"})
            ) + candidato[5]
            if re.fullmatch(r"[A-Z]{3}\\d{2}[A-Z0-9]", candidato):
                return candidato
        return ""''',
        '''    @staticmethod
    def limpiar_placa(texto: str) -> str:
        limpio = re.sub(r"[^A-Z0-9]", "", texto.upper())
        # Colombian motorcycle plate: exactly 3 letters, 2 digits, 1 letter.
        # Do not slide over longer words such as COLOMBIA.
        if len(limpio) == 7 and re.fullmatch(r"[A-Z]{4}\\d{2}[A-Z]", limpio):
            # EasyOCR can insert one false letter at the letter/digit boundary.
            limpio = limpio[:3] + limpio[4:]
        if len(limpio) != 6 or not re.fullmatch(r"[A-Z]{3}[A-Z0-9]{2}[A-Z]", limpio):
            return ""
        numeros = limpio[3:5].translate(str.maketrans({
            "O": "0", "Q": "0", "D": "0", "I": "1", "L": "1",
            "Z": "2", "S": "5", "B": "8", "G": "6",
        }))
        candidato = limpio[:3] + numeros + limpio[5]
        return candidato if re.fullmatch(r"[A-Z]{3}\\d{2}[A-Z]", candidato) else ""''',
    ),
    (
        '''                margen_x, margen_y = int((x2 - x1) * 0.08), int((y2 - y1) * 0.08)
                x1, y1 = max(0, x1 - margen_x), max(0, y1 - margen_y)
                x2, y2 = min(ancho, x2 + margen_x), min(alto, y2 + margen_y)''',
        '''                # Keep OCR inside the detected plate; margins bring in body text.
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(ancho, x2), min(alto, y2)''',
    ),
    (
        '''        # Keep the complete frame as a fallback for missed detections.
        regiones.append(imagen)''',
        '''        # With a plate-specific model, no detection means no OCR candidate.
        # Reading the whole scene can turn the small word COLOMBIA into a plate.
        if not regiones and not any("plate" in str(name).lower() for name in self.model.names.values()):
            regiones.append(imagen)''',
    ),
    (
        '''            for variante in variantes:
                texto = "".join(self.reader.readtext(variante, detail=0, allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))
                placa = self.limpiar_placa(texto)
                if placa:
                    return placa''',
        '''            for variante in variantes:
                lecturas = self.reader.readtext(
                    variante, detail=1, paragraph=False,
                    allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", decoder="greedy",
                )
                alto_variante = variante.shape[0]
                candidatas = []
                for caja_texto, texto, confianza in lecturas:
                    centro_y = sum(punto[1] for punto in caja_texto) / len(caja_texto)
                    # "COLOMBIA" is printed in a separate, lower row on the plate.
                    if centro_y >= alto_variante * 0.72 or confianza < 0.20:
                        continue
                    placa = self.limpiar_placa(texto)
                    if placa:
                        candidatas.append((float(confianza), placa))
                if candidatas:
                    return max(candidatas, key=lambda item: item[0])[1]''',
    ),
]

for old, new in patches:
    if old not in text:
        raise SystemExit("VisionService changed; staging patch could not be applied safely")
    text = text.replace(old, new, 1)

target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(text, encoding="utf-8")
print(target)
