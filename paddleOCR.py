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
            mat = fitz.Matrix(2, 2)
            pm = page.get_pixmap(matrix=mat, alpha=False)
            # if width or height > 2000 pixels, don't enlarge the image
            if pm.width > 2000 or pm.height > 2000:
                pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            imgs.append(img)

    cnt = 0
    txt = ""
    for img in imgs:
        result = ocr.ocr(img, cls=False, det=True)[0]
        for idx in range(len(result)):
            res = result[idx]
            txt = txt + res[1][0] + "\n"
        cnt = cnt + 1
        # perform write operation every ten pages
        if cnt >= 10:
            f = open(f'./output/{filename}.txt', 'a')
            f.write(txt)
            cnt = 0
            txt = ""
    # the last one write operation
    f = open(f'./output/{filename}.txt', 'a')
    f.write(txt)