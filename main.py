import argparse
import os

import torch
from lavis.models import registry, load_preprocess, OmegaConf
import numpy as np
from paddleocr import PaddleOCR

from ImageCaptions import ImageCaption
from ImageExtract import ImageExtractor
from PageProcess import toImage
from Reconstruction import reconstruct
from TextTypeset import textTypeset



def main(appid: str, appkey: str):
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=True,
                    lang="ch", show_log=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cfg = OmegaConf.load("model.yaml")
    vis_processors, _ = load_preprocess(cfg.preprocess)
    model_cls = registry.get_model_class("blip_caption")
    model = model_cls.from_config(cfg.model)
    model.eval()
    model = model.to(device)

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
        txt_captions = []
        pages = toImage(book_path)
        for i in range(len(pages)):
            print(f'Processing page {i}')
            page = pages[i]
            h, w, d = np.shape(page)
            result = ocr.ocr(page, cls=False)[0]
            # extract images and their areas from pages
            img_areas, imgs = ImageExtractor(page, result)
            # text typeset
            textTypeset(result, bookname, img_areas, h, w)
            # image-caption
            txt_caption = ImageCaption(model, vis_processors, imgs, appid, appkey)
            txt_captions += txt_caption
        # conbine txt_captions and txt-file
        reconstruct(txt_captions, bookname)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Your baidu translation API account')
    parser.add_argument('--id', type=str)
    parser.add_argument('--key', type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # args=parse_args()
    # main(args.id,args.key)
    main("20221116001456044", "csyVeF17Gwuyoc26bGgp")
