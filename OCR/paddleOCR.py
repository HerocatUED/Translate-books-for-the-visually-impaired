from paddleocr import PaddleOCR

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
# need to run only once to download and load model into memory
ocr = PaddleOCR(use_angle_cls=True, use_gpu=False,
                lang="ch", page_num=1, show_log=False)
img_path = './OCR/test.pdf'
result = ocr.ocr(img_path, cls=True, det=True)
txt = ""
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        txt = txt+line[1][0]+"\n"
f = open('./OCR/test.txt', 'w')
f.write(txt)


