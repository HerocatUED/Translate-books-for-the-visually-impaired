import os
from DataPreproduce import preproduce
from MyOCR import OCR
from ImageSegmentation import ImageSegment

book_paths = os.listdir('input')
for book_path in book_paths:
    bookname = book_path[:-4]
    pages=preproduce(book_path)
    img_coordinates,imgs=ImageSegment(pages)
    OCR(pages,bookname,img_coordinates)
    # txt_captions = ImageCaption(imgs)
    # reconstruct(txt_captions,bookname)