from ImageExtract import Area


def textTypeset(result, filename: str, img_areas: Area):
    txt = ""
    label = "%&%$\n"
    f = open(f'./output/{filename}.txt', 'w')
    if len(result) == 0:
        if len(img_areas):
            txt = txt + label
            f.write(txt)
            return
        else:
            return
    for idx in range(len(result)):
        txt = txt + result[idx][1][0] + "\n"
    # insert image labels
    for area in img_areas:
        flag = False
        for idx in range(len(result)):
            if area.y1 < result[idx][0][3][1]:
                tmp = result[idx][1][0] + "\n"
                if len(tmp) > 5:
                    pos = txt.find(tmp) + len(tmp)
                    txt = txt[:pos] + label + txt[pos:]
                    flag = True
                    break
        if not flag:
            txt = txt + label
    # perform write operation every page
    f.write(txt)
    f.close()
