import os
from paddleocr import PaddleOCR
from DataPreprocess import preprocess
from ImageExtract import ImageExtractor
from TextTypeset import textTypeset
from ImageCaptions import ImageCaption
from Reconstruction import reconstruct


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
    # text typeset
    textTypeset(results, bookname, img_areas)
    # image-caption
    txt_captions = ImageCaption(imgs)
    # conbine txt_captions and txt-file
    reconstruct(txt_captions, bookname)
