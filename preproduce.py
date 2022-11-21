from paddleocr import PaddleOCR
from PIL import Image
import cv2
import fitz
import numpy as np
import os

ocr = PaddleOCR(use_angle_cls=False, use_gpu=True,
                lang="ch", show_log=False)

img_paths = os.listdir('input')

for img_path in img_paths:

    filename = img_path[:-4]
    imgs = []

    with fitz.open(f'./input/{img_path}') as pdf:
        for pg in range(0, pdf.pageCount):
            page = pdf[pg]
            pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            pm = page.get_pixmap(matrix=fitz.Matrix(
                2000/pm.height, 2000/pm.height), alpha=False)
            img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            imgs.append(img)

    cnt = 0
    txt = ""
    f = open(f'./output/{filename}.txt', 'a')
    for img in imgs:
        result = ocr.ocr(img, cls=False, det=True)[0]
        for idx in range(len(result)):
            if not result[idx]:
                continue
            txt = txt + result[idx][1][0] + "\n"
            
        cnt = cnt + 1
        # perform write operation every ten pages
        if cnt >= 10:
            f.write(txt)
            cnt = 0
            txt = ""
    # the last one write operation
    f.write(txt)
