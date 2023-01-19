import json
import os

from PIL import Image


def txt_to_coco(img_path: str, txt_path: str, coco_path: str):
    os.makedirs(os.path.join(coco_path, "annotations"), exist_ok=True)
    path = os.listdir(img_path)
    imgs=[]
    for img in path:
        if not img[-3:] == "png":
            continue
        imgs.append(img)
    imgs.sort(key=lambda x: x[:-10])
    f = open(txt_path, "r", encoding="utf-8", errors='ignore')
    annotations = []
    id = 0
    for img in imgs:
        caption = f.readline()
        caption=caption.strip("\n")
        annotations.append({"caption":caption,"image":"val2017/"+img,"image_id":str(id)})
        id += 1
    with open(os.path.join(coco_path, "annotations/captions_karpathy_val.json"), 'w') as output:
        json.dump(annotations, output,ensure_ascii=False)
    output.close()


if __name__ == "__main__":
    img_path = "English/images/val2017"
    txt_path = "English/images/val2017/val.txt"
    coco_path = "English"
    txt_to_coco(img_path, txt_path, coco_path)
