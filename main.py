import os
from DataPreproduce import preproduce
from MyOCR import OCR
from ImageSegmentation import *

book_paths = os.listdir('input')
for book_path in book_paths:
    # if book xxx.pdf, bookname = xxx
    bookname = book_path[:-4]
    # convert scanned pdf file to pictures
    pages = preproduce(book_path)
    # extract images and their areas from pages
    img_areas, imgs = ImageSegment(pages)
    # OCR operation
    OCR(pages, bookname, img_areas)

    # txt_captions = ImageCaption(imgs)
    # reconstruct(txt_captions,bookname)
