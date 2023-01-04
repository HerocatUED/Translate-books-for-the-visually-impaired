from paddleocr import PaddleOCR
import numpy as np

def OCR(imgs,filename,coordinates):
    ocr = PaddleOCR(use_angle_cls=False, use_gpu=True,
                lang="ch", show_log=False)
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
