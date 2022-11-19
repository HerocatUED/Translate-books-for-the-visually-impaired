from paddleocr import PaddleOCR
from PIL import Image
import cv2
import fitz
import numpy as np

ocr = PaddleOCR(use_angle_cls=True, use_gpu=True,
                lang="ch", page_num=2, show_log=False)

img_path = './Datasets/敦煌奇幻旅行记1/1-68.pdf'

imgs = []
with fitz.open(img_path) as pdf:
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        mat = fitz.Matrix(2, 2)
        pm = page.getPixmap(matrix=mat, alpha=False)
        # if width or height > 2000 pixels, don't enlarge the image
        if pm.width > 2000 or pm.height > 2000:
            pm = page.getPixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        imgs.append(img)

result = ocr.ocr(imgs[10], cls=True, det=True)

txt = ""
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        txt = txt+line[1][0]+"\n"
f = open('./OCR/test.txt', 'w')
f.write(txt)
