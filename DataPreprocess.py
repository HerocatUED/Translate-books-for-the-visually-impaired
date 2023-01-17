import os
import cv2
from paddleocr import PaddleOCR
from PageProcess import toImage
from TextTypeset import textTypeset
from ImageExtract import *


book_paths = os.listdir('input')
labels = {'敦煌奇幻旅行记1': '插图，', '五三班的坏小子': '插图：', 'test': '插图'}
encode = {'敦煌奇幻旅行记1': 'utf-8', '五三班的坏小子': 'gbk', 'test': 'utf-8'}


def extract_img():
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=True,
                    lang="ch", show_log=False)
    j = 0
    for book_path in book_paths:
        if not book_path[-3:] == "pdf":
            continue
        # if book xxx.pdf, bookname = xxx
        bookname = book_path[:-4]
        # convert scanned pdf file to pictures
        print(f"Processing {bookname}")
        pages = toImage(book_path)
        for i in range(len(pages)):
            print(f'Processing page {i}')
            page = pages[i]
            result = ocr.ocr(page, cls=False)[0]
            # extract images and their areas from pages
            img_areas, imgs = ImageExtractor(page, result)
            # text typeset
            textTypeset(result, bookname, img_areas)
            for img in imgs:
                cv2.imwrite(f'./output/{bookname}/{j}_image.png', img)
                j += 1


def extract_txt():
    i = 0
    for book_path in book_paths:
        if not book_path[-3:] == "txt":
            continue
            # if book xxx.pdf, bookname = xxx
        bookname = book_path[:-4]
        f = open(f'./input/{book_path}', "r",
                 encoding=encode[bookname], errors='ignore')
        lines = f.readlines()
        f.close()
        f = open(f'./output/{bookname}/caption.txt', 'a')
        for line in lines:
            pos = line.find(labels[bookname])
            if not pos == -1:
                f.write(line[pos+len(labels[bookname]):]+'\n')
        i += 1
        f.close()


def main():
    extract_txt()
    extract_img()


if __name__ == '__main__':
    main()
