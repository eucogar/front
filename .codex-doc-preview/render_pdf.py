from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageOps, ImageDraw
pdf=pdfium.PdfDocument(r'C:\Users\euco\Desktop\PROYECTO\front\.codex-doc-preview\protocol-review.pdf')
out=Path(r'C:\Users\euco\Desktop\PROYECTO\front\.codex-doc-preview\rendered')
out.mkdir(parents=True,exist_ok=True)
thumbs=[]
for i in range(len(pdf)):
 page=pdf[i]; bitmap=page.render(scale=1.25); img=bitmap.to_pil(); path=out/f'page-{i+1:02}.png'; img.save(path)
 thumb=img.copy(); thumb.thumbnail((400,560)); canvas=Image.new('RGB',(420,600),'white'); canvas.paste(thumb,((420-thumb.width)//2,25)); ImageDraw.Draw(canvas).text((12,6),f'Page {i+1}',fill='black'); thumbs.append(canvas)
for start in range(0,len(thumbs),8):
 batch=thumbs[start:start+8]; sheet=Image.new('RGB',(1680,1200),'#dddddd')
 for j,im in enumerate(batch): sheet.paste(im,((j%4)*420,(j//4)*600))
 sheet.save(out/f'contact-{start//8+1:02}.jpg',quality=88)
print('pages',len(pdf),'images',len(list(out.glob('page-*.png'))),'sheets',len(list(out.glob('contact-*.jpg'))))
