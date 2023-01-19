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
    images = []
    annotations = []
    licenses = []
    id = 0
    for img in imgs:
        im = Image.open(os.path.join(img_path, img))
        image = {"id": id, "width": im.width, "height": im.height, "file_name": img, "license": 0,
                 "flickr_url": '', "coco_url": '', "date_captured": '2023-1-20 23:59:59', }
        caption = f.readline().strip("\n")
        annotation = {"image_id": id, "id": id, "caption": caption}
        images.append(image)
        annotations.append(annotation)
        licenses.append({"id": id, "name": '', "url": '', })
        id += 1

    annotation = {"info": {"year": 2023, "version": '1.0', "description": "Accessible Book Caption Dataset",
                           "contributor": 'Lumiere Team', "url": '', "date_created": '2023-1-20 23:59:59', },
                  "images": images, "annotations": annotations, "licenses": licenses, }
    with open(os.path.join(coco_path, "annotations/captions_train2017.json"), 'w') as output:
        json.dump(annotation, output, separators=(',', ': '),ensure_ascii=False)
    output.close()


if __name__ == "__main__":
    img_path = "English/images/train2017"
    txt_path = "English/images/train2017/train.txt"
    coco_path = "English"
    txt_to_coco(img_path, txt_path, coco_path)
