import json
import os

from PIL import Image


def txt_to_coco(img_path: str, txt_path: str, coco_path: str):
    os.makedirs(os.path.join(coco_path, "annotations"), exist_ok=True)
    imgs = os.listdir(img_path)
    imgs.sort(key=lambda x: x[:-4])
    f = open(txt_path, "r", encoding="utf-8", errors='ignore')
    images = []
    annotations = []
    licenses = []
    id = 0
    for img in imgs:
        if not img[-3:] == "png":
            continue
        im = Image.open(os.path.join(img_path, img))
        image = {"id": id, "width": im.width, "height": im.height, "file_name": img, "license": 0,
                 "flickr_url": '', "coco_url": '', "date_captured": '2023-1-20 23:59:59', }
        caption = f.readline()
        annotation = {"image_id": id, "id": id, "caption": caption}
        images.append(image)
        annotations.append(annotation)
        licenses.append({"id": id, "name": '', "url": '', })
        id += 1

    annotation = {"info": {"year": 2023, "version": '1.0', "description": "Accessible Book Caption Dataset",
                           "contributor": 'Lumière Team', "url": '', "date_created": '2023-1-20 23:59:59', },
                  "images": images, "annotations": annotations, "licenses": licenses, }
    with open(os.path.join(coco_path, "annotations/captions_train2017.json"), 'w') as output:
        json.dump(annotation, output, separators=(',', ': '))
    output.close()


if __name__ == "__main__":
    img_path = "output/old/怪物危机"
    txt_path = "output/old/怪物危机/caption.txt"
    coco_path = "temp_coco"
    txt_to_coco(img_path, txt_path, coco_path)
