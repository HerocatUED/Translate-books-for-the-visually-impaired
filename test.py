import os
import cv2
from paddleocr import PaddleOCR
from DataPreprocess import preprocess
from ImageExtract import *

ocr = PaddleOCR(use_angle_cls=True, use_gpu=True,
                lang="ch", show_log=False)
book_paths = os.listdir('input')
for book_path in book_paths:
    if not book_path[-3:] == "pdf":
        continue
    # if book xxx.pdf, bookname = xxx
    bookname = book_path[:-4]
    # convert scanned pdf file to pictures
    pages = preprocess(book_path)
    img_areas = []  # [[page1: area1,area2,...],[page2: area1,area2,...], ...]
    imgs = []  # [img1,img2,img3, ...]
    results = []  # [result1,result2, ...]
    for page in pages:
        result = ocr.ocr(page, cls=False)[0]
        # extract images and their areas from pages
        img_area, pictures = ImageExtractor(page, result)
        img_areas.append(img_area)
        imgs += pictures
        results.append(result)
    i = 0
    for img in imgs:
        cv2.imwrite(f'./output/image{i}.png', img)
        i += 1
    print(len(imgs))