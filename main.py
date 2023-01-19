import os
import argparse
from paddleocr import PaddleOCR
from PageProcess import toImage
from ImageExtract import ImageExtractor
from TextTypeset import textTypeset
from ImageCaptions import ImageCaption
from Reconstruction import reconstruct

def main(appid: str, appkey: str):
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=True,
                    lang="ch", show_log=False)
    book_paths = os.listdir('input')
    for book_path in book_paths:
        if not book_path[-3:] == "pdf":
            continue
        # if book xxx.pdf, bookname = xxx
        bookname = book_path[:-4]
        # cover txt file
        f = open(f'./output/{bookname}.txt', 'w')
        f.write("")
        f.close()
        # convert scanned pdf file to pictures
        print(f"Processing {bookname}")
        txt_captions=[]
        pages = toImage(book_path)
        for i in range(len(pages)):
            print(f'Processing page {i}')
            page=pages[i]
            result = ocr.ocr(page, cls=False)[0]
            # extract images and their areas from pages
            img_areas, imgs = ImageExtractor(page, result)
            # text typeset
            textTypeset(result, bookname, img_areas)
            # image-caption
            txt_caption = ImageCaption(imgs,appid, appkey)
            txt_captions+=txt_caption
        # conbine txt_captions and txt-file
        reconstruct(txt_captions, bookname)

def parse_args():
    parser = argparse.ArgumentParser(description='Your baidu translation API account')
    parser.add_argument('--id', type=str)
    parser.add_argument('--key', type=str)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args=parse_args()
    main(args.id,args.key)