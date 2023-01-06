
def reconstruct(txt_captions,bookname:str):
    f = open(f'./output/{bookname}.txt', 'rw')
    lines = f.readlines()
    f.close()
    f = open(f'./output/{bookname}.txt', '')
    f.write("") # cover old version
    f.close()
    f = open(f'./output/{bookname}.txt', 'a')
    lable = "%&%$"
    new_file = ""
    cnt = len(lines)
    idx = 0
    for txt_caption in txt_captions:
        while idx < cnt and lines[idx].find(lable) == -1:
            idx = idx + 1
            new_file = new_file+lines[idx]
        new_file = new_file + "插图：" + lines[idx].replace(lable,txt_caption)
        f.write(new_file)
        new_file = ""
    f.close()
    