import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const SKILL_DIR = 'C:/Users/euco/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const RUNTIME_NODE_MODULES = 'C:/Users/euco/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const RUNTIME_PYTHON = 'C:/Users/euco/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const workspaceDir = 'C:/Users/euco/Desktop/PROYECTO/front';
const sourcePath = path.join(workspaceDir, 'deliverables/Sustentacion_Acceso_Vehicular_UPC_con_resultados.pptx');
const finalPath = path.join(workspaceDir, 'deliverables/Sustentacion_Acceso_Vehicular_UPC_metricas_Oct2026_final.pptx');
const candidatePath = path.join(workspaceDir, '.codex-pptx-build/staging/candidate.pptx');
const screenshotPath = 'C:/Users/euco/AppData/Local/Temp/codex-clipboard-83b9a1d2-7925-4579-bba4-842ce74a5c6a.jpg';
const backgroundPath = path.join(workspaceDir, '.codex-pptx-build/media/image20.jpeg');
const metricReportPath = path.join(workspaceDir, 'deliverables/test_modelo_vision_20261012.json');
const fontPolicy = {
  basis: 'reference',
  families: ['Calibri'],
  referencePath: sourcePath,
  referenceSha256: '8e49d818cc5aec4d45381a3b1dfe14e96ad8839131b8fc630e021ac045d69f9d',
};

const { FileBlob, PresentationFile } = await import(pathToFileURL(path.join(RUNTIME_NODE_MODULES, '@oai/artifact-tool', 'dist', 'artifact_tool.mjs')).href);
const presentation = await PresentationFile.importPptx(await FileBlob.load(sourcePath));
const metricReport = JSON.parse(await fs.readFile(metricReportPath, 'utf8'));
const backgroundBytes = new Uint8Array(await fs.readFile(backgroundPath));
const screenshotBytes = new Uint8Array(await fs.readFile(screenshotPath));
const initialSlides = await presentation.inspect({ kind: 'slide', maxChars: 50000 });
const originalSlideIds = initialSlides.ndjson.split('\n').filter(Boolean).map(line => JSON.parse(line).id);

// Update the earlier OCR slide so it reads as a historical baseline rather than the new detector result.
presentation.resolve('sh/rq50vmp8').text = 'Prueba inicial del OCR con modelo base';
presentation.resolve('sh/3ml0rmpw').text = 'Resultado del piloto inicial';
presentation.resolve('sh/gjuhg7ql').text = 'Referencias manuales: WUF62C y HXF05F\nModelo YOLOv8n COCO sin ajuste\nCoincidencia exacta: 0/2 fotos\n10 repeticiones: 0/10 exactas\nLecturas: WUF262 y XFS05F';
presentation.resolve('sh/cj65wzyd').text = 'Prueba local en CPU';
presentation.resolve('sh/rid4nuhs').text = 'Mediana: 5,62 s por imagen\np95: 8,39 s por imagen\nMedia: 5,55 s por imagen\nYOLOv8n base + EasyOCR\nInicio excluido';
presentation.resolve('sh/pwvmlkzm').text = 'Resultado histórico anterior al entrenamiento; no describe el detector evaluado a continuación.';

// Update the methodology status with the measured held-out detector evaluation.
presentation.resolve('sh/cva9k7a9').text = 'Estado: detector medido en test; OCR exacto y pruebas de campo siguen pendientes.';
presentation.resolve('nt/m90b6t0r').text = [
  'El proyecto propone Scrum, pruebas funcionales y métricas de visión artificial. Actualización del 12 de octubre de 2026: el detector de cajas de placas se evaluó sobre el split test reservado. La exactitud OCR de seis caracteres y las pruebas en cámaras del campus siguen pendientes de una muestra etiquetada representativa.',
  `Reporte reproducible: ${metricReportPath}`,
].join('\n');

function addText(slide, name, text, position, style = {}) {
  const shape = slide.shapes.add({
    geometry: 'textbox',
    name,
    position,
    fill: 'none',
    line: { style: 'solid', fill: 'none', width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    typeface: 'Calibri',
    fontSize: 24,
    color: '#17243A',
    alignment: 'left',
    ...style,
  };
  shape.text.insets = 0;
  return shape;
}

function addCard(slide, x, y, width, height, accent) {
  slide.shapes.add({
    geometry: 'roundRect',
    position: { left: x, top: y, width, height },
    fill: '#FFFFFF',
    line: { style: 'solid', fill: '#D8E1EB', width: 1.5 },
    borderRadius: 22,
  });
  slide.shapes.add({
    geometry: 'rect',
    position: { left: x, top: y, width: 12, height },
    fill: accent,
    line: { style: 'solid', fill: accent, width: 1 },
  });
}

function addTemplate(slide, section, title, note) {
  slide.background.fill = '#FFFFFF';
  slide.images.add({
    blob: backgroundBytes,
    contentType: 'image/jpeg',
    alt: 'Fondo institucional UPC',
    fit: 'cover',
    position: { left: 0, top: 0, width: 1920, height: 1080 },
  });
  addText(slide, 'section-heading', section, { left: 420, top: 70, width: 1140, height: 38 }, {
    fontSize: 22, color: '#0876B9', bold: true,
  });
  addText(slide, 'slide-title', title, { left: 420, top: 170, width: 1370, height: 80 }, {
    fontSize: 46, color: '#0876B9', bold: true,
  });
  addText(slide, 'slide-footer', 'Acceso vehicular UPC  ·  Ingeniería de Sistemas', { left: 105, top: 1000, width: 950, height: 28 }, {
    fontSize: 18, color: '#526176',
  });
  slide.speakerNotes.text = note;
}

// Add measured detector results after the historical OCR pilot.
const metricsSlide = presentation.slides.add({ width: 1920, height: 1080, background: { fill: '#FFFFFF' } });
addTemplate(
  metricsSlide,
  '9. VALIDACIÓN DEL MODELO',
  'Evaluación del detector de placas',
  [
    `Evaluación ejecutada el ${metricReport.generated_at} con los pesos desplegados en VisionArtificial/plate_detector.pt.`,
    `Conjunto: Roboflow ${metricReport.dataset}, split test reservado; ${metricReport.images} imágenes, 67 objetos anotados y 34 imágenes de fondo.`,
    `Precisión ${ (metricReport.metrics.precision * 100).toFixed(2) }%; recall ${ (metricReport.metrics.recall * 100).toFixed(2) }%; mAP@50 ${ (metricReport.metrics.map50 * 100).toFixed(2) }%; mAP@50–95 ${ (metricReport.metrics.map50_95 * 100).toFixed(2) }%.`,
    `Tiempos por imagen en RTX 3060: inferencia ${metricReport.metrics.speed_ms_per_image.inference} ms; preprocesamiento ${metricReport.metrics.speed_ms_per_image.preprocess} ms; postprocesamiento ${metricReport.metrics.speed_ms_per_image.postprocess} ms. La inferencia no representa latencia de extremo a extremo.`,
    'Fuente del dataset: Roboflow Universe, Detection Colombian Moto Plates, versión 15, licencia CC BY 4.0. https://universe.roboflow.com/itm-n1i3r/detectioncolombianmotoplates-6o1aj/dataset/15',
    `Huella SHA-256 del modelo: ${metricReport.model_sha256}. Las métricas corresponden a detección de cajas; el dataset no contiene transcripciones OCR completas y no permite calcular exactitud de lectura de caracteres ni desempeño en campus.`,
  ].join('\n'),
);
addCard(metricsSlide, 160, 292, 735, 350, '#0876B9');
addText(metricsSlide, 'metrics-heading', 'Métricas en el conjunto test', { left: 190, top: 316, width: 675, height: 48 }, {
  fontSize: 29, color: '#122A51', bold: true,
});
addText(metricsSlide, 'metrics-values',
  `Precisión de detección     ${(metricReport.metrics.precision * 100).toFixed(1).replace('.', ',')} %\nRecall                              ${(metricReport.metrics.recall * 100).toFixed(1).replace('.', ',')} %\nmAP@50                           ${(metricReport.metrics.map50 * 100).toFixed(1).replace('.', ',')} %\nmAP@50–95                     ${(metricReport.metrics.map50_95 * 100).toFixed(1).replace('.', ',')} %`,
  { left: 190, top: 390, width: 675, height: 220 },
  { fontSize: 28, color: '#17243A' },
);
addCard(metricsSlide, 1000, 292, 735, 350, '#F28C28');
addText(metricsSlide, 'conditions-heading', 'Muestra y equipo', { left: 1030, top: 316, width: 675, height: 48 }, {
  fontSize: 29, color: '#122A51', bold: true,
});
addText(metricsSlide, 'conditions-values', '101 imágenes de prueba\n67 placas anotadas · 34 fondos\nYOLOv8n ajustado · 640 px\nNVIDIA RTX 3060 · CUDA 12.8\nInferencia: 4,93 ms por imagen',
  { left: 1030, top: 390, width: 675, height: 220 },
  { fontSize: 27, color: '#17243A' },
);
metricsSlide.shapes.add({
  geometry: 'roundRect',
  position: { left: 250, top: 710, width: 1420, height: 126 },
  fill: '#EEF6FB',
  line: { style: 'solid', fill: '#C8D9E8', width: 1.5 },
  borderRadius: 22,
});
addText(metricsSlide, 'metrics-limitation', 'Las métricas evalúan la localización de cajas. No miden exactitud OCR ni desempeño en las cámaras del campus.',
  { left: 300, top: 744, width: 1320, height: 70 },
  { fontSize: 25, color: '#122A51', bold: true, alignment: 'center' },
);

// Add a privacy-safe crop of the user-provided application screenshot as product evidence.
const interfaceSlide = presentation.slides.add({ width: 1920, height: 1080, background: { fill: '#FFFFFF' } });
addTemplate(
  interfaceSlide,
  '8. PRESENTACIÓN DEL PRODUCTO',
  'Registro de acceso desde el aplicativo',
  'Captura de interfaz proporcionada por el usuario. Se recortó el área inferior que contenía identificación y resultados anteriores. La imagen muestra el formulario de registro y carga de fotografía; el módulo de cámara en vivo funciona como una pantalla independiente.',
);
addText(interfaceSlide, 'interface-summary-heading', 'Flujo para el operador', { left: 180, top: 330, width: 690, height: 55 }, {
  fontSize: 34, color: '#122A51', bold: true,
});
addText(interfaceSlide, 'interface-summary', 'Identifica a la persona autorizada.\n\nCarga una imagen de la placa o escribe el dato manualmente.\n\nEn cámara en vivo, el operador solicita la lectura con Enter y confirma antes de registrar el movimiento.',
  { left: 185, top: 415, width: 700, height: 360 },
  { fontSize: 29, color: '#526176' },
);
interfaceSlide.images.add({
  blob: screenshotBytes,
  contentType: 'image/jpeg',
  alt: 'Formulario móvil de registro de entrada o salida; se omiten identificación y resultado OCR',
  fit: 'contain',
  crop: { left: 0, top: 0.35, right: 0, bottom: 0.23 },
  geometry: 'roundRect',
  borderRadius: 18,
  position: { left: 980, top: 300, width: 600, height: 560 },
});
addText(interfaceSlide, 'interface-caption', 'Formulario de registro · datos personales excluidos', { left: 980, top: 875, width: 650, height: 42 }, {
  fontSize: 19, color: '#526176', alignment: 'center',
});

const updatedSlides = await presentation.inspect({ kind: 'slide', maxChars: 60000 });
const slideRecords = updatedSlides.ndjson.split('\n').filter(Boolean).map(line => JSON.parse(line));
const metricsSlideId = slideRecords.find(record => record.kind === 'slide' && record.slideIndex === 23).id;
const interfaceSlideId = slideRecords.find(record => record.kind === 'slide' && record.slideIndex === 24).id;
presentation.slides.reorder([
  ...originalSlideIds.slice(0, 20),
  metricsSlideId,
  interfaceSlideId,
  ...originalSlideIds.slice(20),
]);

await fs.mkdir(path.dirname(candidatePath), { recursive: true });
await fs.mkdir(path.dirname(finalPath), { recursive: true });
const candidate = await PresentationFile.exportPptx(presentation);
await candidate.save(candidatePath);

const { finalizePresentation } = await import(pathToFileURL(path.join(SKILL_DIR, 'container_tools/artifact_tool_utils.mjs')).href);
const stagingDir = path.dirname(candidatePath);
const result = await finalizePresentation({
  explicitTotalSlideCount: 25,
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: RUNTIME_PYTHON,
  integrityValidatorPath: path.join(SKILL_DIR, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(SKILL_DIR, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '18288000,10287000', '--validate-bullet-geometry', '--validate-heading-fit'],
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [],
  fontPolicy,
  verifyArtifactToolImport: true,
  receiptPath: path.join(stagingDir, 'Sustentacion_Acceso_Vehicular_UPC_metricas_Oct2026_final.validation.json'),
});
console.log(JSON.stringify(result, null, 2));
console.log('FINAL', finalPath);
