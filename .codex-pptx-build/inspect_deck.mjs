import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const runtimeModules = 'C:/Users/euco/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const { FileBlob, PresentationFile } = await import(pathToFileURL(path.join(runtimeModules, '@oai/artifact-tool', 'dist', 'artifact_tool.mjs')).href);
const source = 'C:/Users/euco/Desktop/PROYECTO/front/deliverables/Sustentacion_Acceso_Vehicular_UPC_con_resultados.pptx';
const out = 'C:/Users/euco/Desktop/PROYECTO/front/.codex-pptx-build/source-preview';
await fs.mkdir(out, { recursive: true });
const presentation = await PresentationFile.importPptx(await FileBlob.load(source));
console.log('slides', presentation.slides.items.length);
const report = await presentation.inspect({ kind: 'slide,textbox,shape,image,table,chart,notes,layout', maxChars: 400000 });
await fs.writeFile(path.join(out, 'inspection.ndjson'), report.ndjson, 'utf8');
const resultSlide = await presentation.inspect({ kind: 'slide,textbox,shape,image,notes', search: 'Prueba piloto de reconocimiento de placas', maxChars: 20000 });
await fs.writeFile(path.join(out, 'result-slide.ndjson'), resultSlide.ndjson, 'utf8');
for (let index = 0; index < presentation.slides.items.length; index += 1) {
  const slide = presentation.slides.items[index];
  if (index >= 13 && index <= 20) {
    const png = await presentation.export({ slide, format: 'png', scale: 1 });
    await fs.writeFile(path.join(out, `slide-${String(index + 1).padStart(2, '0')}.png`), new Uint8Array(await png.arrayBuffer()));
  }
}
const montage = await presentation.export({ format: 'webp', montage: true, scale: 0.4 });
await fs.writeFile(path.join(out, 'montage.webp'), new Uint8Array(await montage.arrayBuffer()));
console.log('wrote', out);
