from PIL import Image
import cv2
import fitz
import numpy as np
import os
import OCR

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

    img_coordinates=[]
    OCR(imgs,filename,img_coordinates)
    