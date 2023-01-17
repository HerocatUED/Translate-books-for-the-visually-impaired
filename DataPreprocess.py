import os
import cv2
from paddleocr import PaddleOCR
from PageProcess import toImage
from ImageExtract import *
from TextTypeset import textTypeset


def extract_img():
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=True,
                    lang="ch", show_log=False)
    book_paths = os.listdir('Data_img')
    j = 0
    for book_path in book_paths:
        if not book_path[-3:] == "pdf":
            continue
        # if book xxx.pdf, bookname = xxx
        bookname = book_path[:-4]
        # convert scanned pdf file to pictures
        pages = toImage(book_path)
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
        for img in imgs:
            cv2.imwrite(f'./output/{j}_image.png', img)
            j += 1


def extract_txt():
    book_paths = os.listdir('Data_txt')
    labels = ['一副插图，','插图']
    i = 0
    j = 0
    for book_path in book_paths:
        if not book_path[-3:] == "txt":
            continue
        f = open(book_path, "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            pos = line.find(labels[i])
            if not pos == -1:
                f = open(f'output/{j}_caption.txt', 'w')
                f.write(line[pos+len(labels[i]):]+'\n')
                f.close()
                j += 1
        i += 1


def main():
    extract_img()
    extract_txt()


if __name__ == '__main__':
    main()
