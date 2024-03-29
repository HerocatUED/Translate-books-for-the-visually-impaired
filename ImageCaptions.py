import random
from hashlib import md5
from typing import List
import torch
import numpy as np
import requests
from PIL import Image



def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def ImageCaption(model,processors,imgs: List[np.ndarray], appid: str, appkey: str) -> List[str]:
    """
    model: a lavis model for image caption
    processors: a vis_processor corresponding to the model
    imgs:a list of ndarray image
    appid: id of baidu translation API
    appkey: key of baidu translation API
    """
    captions = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    from_lang = 'en'
    to_lang = 'zh'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    salt = random.randint(32768, 65536)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    for img in imgs:
        raw_image = Image.fromarray(img)
        image = processors["eval"](raw_image).unsqueeze(0).to(device)
        output = model.generate({"image": image}, use_nucleus_sampling=True)
        query = output[0]
        sign = make_md5(appid + query + str(salt) + appkey)
        payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        captions.append(result['trans_result'][0]['dst'])
    return captions

