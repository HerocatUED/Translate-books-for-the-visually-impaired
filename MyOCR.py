from paddleocr import PaddleOCR
from ImageExtract import Area


def OCR(pages, filename: str, img_areas: Area):  # OCR operation
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=True,
                    lang="ch", show_log=False)
    # if the .txt file exit, cover it
    f = open(f'./output/{filename}.txt', 'w')
    f.write("")
    f.close()
    # OCR
    txt = ""
    label = "%&%$\n"
    f = open(f'./output/{filename}.txt', 'a')
    for i in range(len(pages)):
        page = pages[i]
        areas = img_areas[i]
        result = ocr.ocr(page, cls=False, det=True)[0]
        for idx in range(len(result)):
            txt = txt + result[idx][1][0] + "\n"
        # insert image labels
        for area in areas:
            flag = False
            for idx in range(len(result)):
                if area.y1 < result[idx][0][3][1]:
                    tmp = result[idx][1][0] + "\n"
                    if len(tmp) > 5:
                        pos = txt.find(tmp) + len(tmp)
                        txt = txt[:pos] + label + txt[pos:]
                        flag = True
                        break
            if not flag:
                txt = txt + label
        # perform write operation every page
        f.write(txt)
        txt = ""
    f.close()
