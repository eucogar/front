from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import shutil

source = Path(r'C:\Users\euco\Desktop\PROYECTO\Documentos\PROTOCOLO Proyecto de grado 2026.docx')
out = Path(r'C:\Users\euco\Desktop\PROYECTO\front\deliverables\PROTOCOLO_Proyecto_Grado_2026_actualizado_con_evidencia.docx')
source_capture = Path(r'C:\Users\euco\AppData\Local\Temp\codex-clipboard-83b9a1d2-7925-4579-bba4-842ce74a5c6a.jpg')
preview_dir = Path(r'C:\Users\euco\Desktop\PROYECTO\front\.codex-doc-preview')
preview_dir.mkdir(parents=True, exist_ok=True)
crop_path = preview_dir / 'captura_registro_recortada.jpg'

# Retain only the app's success banner and blank registration controls; exclude CC and OCR output.
with Image.open(source_capture) as im:
    w, h = im.size
    crop = im.crop((int(w*0.04), int(h*0.27), int(w*0.97), int(h*0.78)))
    crop.save(crop_path, quality=92)

doc = Document(source)
paras = doc.paragraphs

def paragraph_index(starts):
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().startswith(starts):
            return i, p
    raise ValueError(f'Paragraph not found: {starts}')

def style_like(p, style_name):
    try:
        p.style = doc.styles[style_name]
    except KeyError:
        pass
    return p

def insert_before(anchor, text, style=None, bold_lead=None):
    p = doc.add_paragraph()
    if style:
        style_like(p, style)
    if bold_lead and text.startswith(bold_lead):
        p.add_run(bold_lead).bold = True
        p.add_run(text[len(bold_lead):])
    else:
        p.add_run(text)
    anchor._p.addprevious(p._p)
    return p

# Add a visible revision note to the title page without implying institutional approval.
for p in doc.paragraphs:
    if p.text.strip() == 'Abril de 2026':
        p.text = 'Octubre de 2026'
        break

# Append measured detector evidence to the Spanish and English abstracts.
_, keywords_es = paragraph_index('Palabras clave:')
es_evidence = insert_before(
    keywords_es,
    'Como evidencia de ejecución, el detector YOLOv8n ajustado se evaluó el 12 de octubre de 2026 sobre el conjunto test reservado: 101 imágenes, con 67 placas anotadas y 34 imágenes de fondo. Obtuvo precisión de detección de 95,6 %, recall de 96,8 %, mAP@50 de 99,0 % y mAP@50–95 de 88,8 %. Estas métricas evalúan la localización de la placa; no equivalen a exactitud de lectura OCR ni a validación en cámaras del campus.'
)
_, keywords_en = paragraph_index('Keywords')
en_evidence = insert_before(
    keywords_en,
    'As execution evidence, the fine-tuned YOLOv8n detector was evaluated on the reserved test split on October 12, 2026: 101 images, including 67 annotated plates and 34 background images. It achieved 95.6% detection precision, 96.8% recall, 99.0% mAP@50, and 88.8% mAP@50–95. These metrics measure plate localization; they are not exact OCR transcription accuracy or validation on campus cameras.'
)
es_evidence.paragraph_format.keep_together = True
en_evidence.paragraph_format.keep_together = True

# Make section 3.3 distinguish completed model testing from planned field evaluation.
replacements = {
    'Una vez implementado el sistema, el análisis de resultados se realizará contrastando los datos recolectados en la fase de pruebas y validación contra las hipótesis formuladas en el Marco Metodológico, mediante los siguientes indicadores:':
    'El análisis distingue los resultados técnicos ya obtenidos de las mediciones de campo que siguen pendientes. La evaluación ejecutada del detector se presenta a continuación; las metas operativas del campus solo podrán contrastarse cuando se complete el piloto autorizado y se recolecten sus datos.',
    'Precisión del reconocimiento (contraste de Hipotesis1): porcentaje de placas correctamente reconocidas por el modelo YOLO sobre la muestra de 359 registros, obtenido a partir de la matriz de confusión y las métricas de precisión, recall, F1-score y mAP. Se espera un valor igual o superior al 90 %.':
    'Desempeño del detector (relacionado con H1): la meta propuesta es alcanzar al menos 90 % de precisión en condiciones reales. El test técnico ejecutado mide cajas de detección y se informa por separado; no acredita por sí solo la meta de lectura exacta de caracteres ni el rendimiento en el campus.',
    'Tiempo de ingreso y salida (contraste de Hipotesis2): comparación de las medias de tiempo del registro manual (línea base levantada en la fase de diagnóstico) frente al registro automático, mediante la prueba t de Student o U de Mann-Whitney según el resultado de la prueba de normalidad, con un nivel de significancia α = 0,05. Se espera una reducción de al menos el 50 %.':
    'Tiempo de ingreso y salida (H2): la reducción objetivo es de al menos 50 %. Esta hipótesis aún no se contrasta: falta recolectar una línea base manual y mediciones con el sistema en un piloto de campo; los milisegundos de inferencia del modelo no representan el tiempo total de atención.',
    'Errores de registro (contraste de Hipotesis3): comparación de la proporción de errores del procedimiento manual frente al sistema automatizado mediante la prueba chi-cuadrado o la prueba z de diferencia de proporciones. Se espera una reducción superior al 80 %.':
    'Errores de registro (H3): la reducción objetivo es superior al 80 %. La hipótesis permanece pendiente hasta contar con registros comparables del proceso manual y del sistema automatizado.',
    'Percepción del personal de vigilancia: análisis de contenido de las entrevistas aplicadas, en torno a la carga operativa, la facilidad de uso del sistema y la supervisión de situaciones de riesgo, triangulado con los resultados cuantitativos anteriores.':
    'Percepción del personal operador: se analizarán entrevistas al personal de vigilancia que utilizará el aplicativo. Los estudiantes no operan el sistema; cualquier encuesta a estudiantes debe limitarse a su experiencia como usuarios del acceso, si se conserva ese objetivo de investigación.',
    'La discusión confrontará estos hallazgos con los resultados esperados descritos en el numeral 2.6 (reducción de tiempos, disminución de errores humanos, incremento de la seguridad y optimización del trabajo de vigilancia), determinando si el sistema implementado cumple, supera o no alcanza las metas planteadas, y explicando las posibles causas de las desviaciones observadas.':
    'La discusión reportará por separado la localización de placas en el conjunto test, la lectura OCR exacta y el desempeño operativo en campo. No se afirmará reducción de tiempos, errores o congestión hasta medirlos con datos comparables y una muestra de campo documentada.'
}
for p in doc.paragraphs:
    old = p.text.strip()
    if old in replacements:
        p.text = replacements[old]

    if old == 'Version: .NET11':
        p.text = 'Versión: .NET 9'
    elif old == 'Version:17.0':
        p.text = 'Versión: SQL Server 2022'
    elif old.startswith('Fase 4. Pruebas y validación (junio):'):
        p.text = 'Fase 4. Pruebas y validación: se completó una evaluación técnica del detector YOLOv8n en el split test reservado (101 imágenes). La validación de OCR exacto, las mediciones de tiempos de acceso y la prueba de campo con la muestra planificada de 359 registros siguen pendientes; no se presentan como actividades ejecutadas.'
    elif old.startswith('Fase 5. Ajustes finales y documentación'):
        p.text = 'Fase 5. Ajustes finales y documentación: consolidar el informe con la evaluación técnica obtenida, completar las validaciones pendientes y documentar los límites del prototipo antes de declarar resultados de operación en el campus.'

_, section_32 = paragraph_index('3.2 DESARROLLO DE LAS FASES')
vision_stack = doc.add_paragraph('Servicio de visión artificial: Python 3.14.8 y Ultralytics 8.4.138 con el detector YOLOv8n ajustado. La evaluación reportada se ejecutó a 640 px con CUDA 12.8; el entorno identificó una GPU NVIDIA RTX 3060.')
section_32._p.addprevious(vision_stack._p)
vision_stack.paragraph_format.space_before = Pt(6)
vision_stack.paragraph_format.space_after = Pt(6)
status = doc.add_paragraph('Estado de ejecución al 12 de octubre de 2026: está disponible el resultado de evaluación del detector sobre el conjunto test. El plan original se conserva como referencia; las pruebas OCR completas y la evaluación operativa de campo no se consideran concluidas.')
_, methodology_intro = paragraph_index('El desarrollo del proyecto se organiza mediante la metodología ágil Scrum')
methodology_intro._p.addnext(status._p)
status.paragraph_format.space_after = Pt(6)

# Replace projected conclusions with evidence-based partial conclusions.
_, p_conclusion_intro = paragraph_index('A partir del desarrollo planteado, se proyectan las siguientes')
p_conclusion_intro.text = 'Conclusiones parciales sustentadas en la evidencia técnica disponible al 12 de octubre de 2026:'
for prefix, text in [
    ('El control manual de acceso vehicular', 'El detector YOLOv8n ajustado fue evaluado en 101 imágenes reservadas para test (67 placas anotadas y 34 fondos). La prueba obtuvo precisión de detección de 95,6 %, recall de 96,8 %, mAP@50 de 99,0 % y mAP@50–95 de 88,8 %.'),
    ('La arquitectura tecnológica seleccionada', 'Estas métricas describen la localización de cajas de placa. No demuestran la transcripción exacta de los caracteres: el conjunto evaluado no contiene transcripciones OCR para medir exactitud por placa.'),
    ('La metodología Scrum', 'La captura del aplicativo muestra el mensaje “Entrada registrada exitosamente” en la interfaz del operador. La imagen documenta la respuesta visual del prototipo; por sí sola no verifica la persistencia en la base de datos ni sustituye una prueba de campo.'),
    ('De cumplirse las hipótesis planteadas', 'La prueba OCR exploratoria anterior sobre dos fotografías obtuvo 0/2 coincidencias exactas. Por su tamaño no es representativa; se requiere un conjunto independiente de placas con transcripciones verificadas para medir OCR.'),
]:
    _, p = paragraph_index(prefix)
    p.text = text

# Replace recommendations with next evidence-building steps.
_, p = paragraph_index('A partir de las conclusiones proyectadas')
p.text = 'A partir de los resultados y límites documentados, se recomiendan las siguientes acciones:'
recommendations = {
    'Monitorear el costo mensual del componente de inferencia': 'Construir un conjunto de prueba OCR con transcripciones verificadas y placas distintas de las usadas para ajustar el modelo; reportar coincidencia exacta por placa y tasa de error por carácter, además de conservar la matriz de confusión del detector.',
    'Capacitar al personal de vigilancia': 'Realizar el piloto únicamente con operadores autorizados y, antes de usar cámaras en el campus, gestionar la autorización institucional y definir información, retención y acceso conforme a las reglas de protección de datos.',
    'Mantener el registro histórico de tiempos': 'Medir latencia integral desde la captura hasta la respuesta del aplicativo por separado del tiempo de inferencia del modelo; registrar dispositivo, condiciones de luz, distancia y fallos de lectura.',
    'Evaluar, en fases posteriores, la extensión del sistema': 'Completar la comparación de tiempos y errores entre el proceso manual y el automatizado con la muestra de campo definida en la metodología. No presentar como resultados obtenidos los valores proyectados hasta terminar esa medición.'
}
for prefix, text in recommendations.items():
    _, p = paragraph_index(prefix)
    p.text = text

_, recommendations_heading = paragraph_index('3.5 RECOMENDACIONES')
recommendations_heading.paragraph_format.page_break_before = True

# Add detailed metric table and a privacy-safe application screenshot before section 3.4.
_, conclusion_heading = paragraph_index('3.4 CONCLUSIONES')
intro = doc.add_paragraph('Evaluación ejecutada del detector de placas')
style_like(intro, 'Normal')
intro.paragraph_format.page_break_before = True
intro.paragraph_format.keep_with_next = True
heading_run = intro.runs[0]
heading_run.bold = True
heading_run.font.size = Pt(12)
heading_run.font.color.rgb = RGBColor(0, 0, 0)
conclusion_heading._p.addprevious(intro._p)
body = doc.add_paragraph(
    'El 12 de octubre de 2026 se evaluó el archivo plate_detector.pt, un YOLOv8n ajustado, sobre el split test reservado de la versión 15 del conjunto DetectionColombianMotoPlates. La evaluación se ejecutó a 640 px en una GPU NVIDIA RTX 3060 (según el entorno registrado). El conjunto contiene 101 imágenes: 67 cajas de placa anotadas y 34 imágenes de fondo.'
)
conclusion_heading._p.addprevious(body._p)

table = doc.add_table(rows=1, cols=2)
table.style = 'Table Grid'
table.rows[0].cells[0].text = 'Indicador'
table.rows[0].cells[1].text = 'Resultado'
for left, right in [
    ('Imágenes analizadas', '101'),
    ('Placas anotadas / fondos', '67 / 34'),
    ('Precisión de detección', '95,6 %'),
    ('Recall', '96,8 %'),
    ('mAP@50 / mAP@50–95', '99,0 % / 88,8 %'),
    ('Inferencia del modelo', '4,93 ms por imagen (solo inferencia)'),
]:
    cells = table.add_row().cells
    cells[0].text = left
    cells[1].text = right
for row in table.rows:
    trPr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement('w:cantSplit')
    trPr.append(cant_split)
conclusion_heading._p.addprevious(table._tbl)

note = doc.add_paragraph(
    'Interpretación y alcance: las métricas evalúan la localización de cajas, no la lectura exacta de caracteres. El reporte agregado no conserva conteos enteros de verdaderos positivos, falsos positivos y placas omitidas; por tanto, no se afirma “X de 67 aciertos”. La inferencia de 4,93 ms no es la latencia completa del servicio. No se ejecutó con estos datos una prueba de OCR exacto ni una validación con cámaras del campus.'
)
conclusion_heading._p.addprevious(note._p)

ocr = doc.add_paragraph(
    'Lectura OCR: en una prueba exploratoria previa de dos fotografías se obtuvieron 0/2 lecturas exactas (0/10 repeticiones). Esta prueba corresponde al flujo OCR inicial, no al test del detector ajustado, y no permite estimar el desempeño general del OCR. Se requiere validarlo con placas etiquetadas con su texto real.'
)
conclusion_heading._p.addprevious(ocr._p)

fig = doc.add_paragraph()
fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = fig.add_run()
run.add_picture(str(crop_path), width=Inches(2.8))
conclusion_heading._p.addprevious(fig._p)
caption = doc.add_paragraph('Figura. Respuesta visual de registro en la interfaz del operador. Captura recortada para excluir los datos identificables y el resultado OCR.')
caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in caption.runs:
    r.italic = True
    r.font.size = Pt(9)
conclusion_heading._p.addprevious(caption._p)
conclusion_heading.paragraph_format.page_break_before = True

# Compact only the bibliography to prevent its final citation from becoming an orphan page.
in_bibliography = False
for p in doc.paragraphs:
    if p.text.strip().startswith('3.6 BIBLIOGRAFIA'):
        in_bibliography = True
        continue
    if in_bibliography:
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for run in p.runs:
            if run.text.strip():
                run.font.size = Pt(10)

# Add execution references as document metadata; leave the approved original untouched.
doc.core_properties.title = 'Protocolo de proyecto de grado actualizado con evidencia técnica'
doc.core_properties.subject = 'Sistema de acceso vehicular UPC: evaluación de detector y evidencia de aplicativo'
# Remove the original document's trailing blank paragraphs so they cannot create an empty final page.
while doc.paragraphs and not doc.paragraphs[-1].text.strip():
    doc._element.body.remove(doc.paragraphs[-1]._p)
out.parent.mkdir(parents=True, exist_ok=True)
doc.save(out)
print(out)
print('paragraphs', len(doc.paragraphs), 'tables', len(doc.tables), 'bytes', out.stat().st_size)
