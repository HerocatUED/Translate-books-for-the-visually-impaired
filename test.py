import os
from DataPreproduce import preproduce
from ImageSegmentation import *

book_paths = os.listdir('input')
for book_path in book_paths:
    # convert scanned pdf file to pictures
    pages=preproduce(book_path)
    # extract images and their coordinates from pages
    img_coordinates,imgs=ImageSegment(pages)
    