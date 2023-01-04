from paddleocr import PaddleOCR
import numpy as np
import os


# OCR operation
def OCR(pages, filename, coordinates):
    ocr = PaddleOCR(use_angle_cls=False, use_gpu=True,
                    lang="ch", show_log=False)
    # if the .txt file exit, recover it
    f = open(f'./output/{filename}.txt', 'w')
    f.write("")
    f.close()
    # OCR 
    txt = ""
    cnt = 0
    f = open(f'./output/{filename}.txt', 'a')
    for page in pages:
        result = ocr.ocr(page, cls=False, det=True)[0]
        for idx in range(len(result)):
            if not result[idx]:
                continue
            txt = txt + result[idx][1][0] + "\n"
        # perform write operation every ten pages
        cnt = cnt+1
        if cnt == 10:
            f.write(txt)
            cnt = 0
            txt = ""
    # perform last one operation
    f.write(txt)
