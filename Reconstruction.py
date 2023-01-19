
def reconstruct(txt_captions,bookname:str):
    f = open(f'./output/{bookname}.txt', 'r')
    lines = f.readlines()
    f.close()
    f = open(f'./output/{bookname}.txt', 'w')
    label = "%&%$"
    new_file = ""
    cnt = len(lines)
    idx = 0
    for txt_caption in txt_captions:
        while idx < cnt and lines[idx].find(label) == -1:
            idx = idx + 1
            new_file = new_file + lines[idx]
        new_file = new_file + "插图：" + lines[idx].replace(label,txt_caption)
        f.write(new_file)
        new_file = ""
    f.close()
    