import os
import cv2
from DataPreproduce import preproduce
from ImageSegmentation import *

book_paths = os.listdir('input')
for book_path in book_paths:
    if not book_path[-3:] == "pdf":
        continue
    # convert scanned pdf file to pictures
    pages=preproduce(book_path)
    # extract images and their coordinates from pages
    img_coordinates,imgs=ImageSegment(pages)
    i=0
    for img in imgs:
        cv2.imwrite(f'./input/image{i}.png',img)
        i=i+1
