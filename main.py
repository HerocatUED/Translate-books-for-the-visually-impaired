import os
from DataPreproduce import preproduce
from MyOCR import OCR
from ImageSegmentation import ImageSegment
from ImageCaptions import ImageCaption
from Reconstruction import reconstruct

book_paths = os.listdir('input')
for book_path in book_paths:
    if not book_path[-3:] == "pdf":
        continue
    # if book xxx.pdf, bookname = xxx
    bookname = book_path[:-4]
    # convert scanned pdf file to pictures
    pages = preproduce(book_path)
    # extract images and their areas from pages
    img_areas, imgs = ImageSegment(pages)
    # OCR operation
    OCR(pages, bookname, img_areas)
    # image-caption
    txt_captions = ImageCaption(imgs)
    # conbine txt_captions and txt-file
    reconstruct(txt_captions, bookname)
