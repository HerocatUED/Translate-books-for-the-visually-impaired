import requests
import random
from hashlib import md5


def translate(src: str, appid: str, appkey: str, from_lang: str = 'zh', to_lang: str = 'en') -> str:
    """
    src: the sentence to be translate
    appid: the ID of baidu translate API
    appkey: the key of baidu translate API
    from_lang: the language translate from,default ch (Chinese)
    to_lang: the language translate to,default en (English)
    """
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + src + str(salt) + appkey)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': src, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    return result['trans_result'][0]['dst']
