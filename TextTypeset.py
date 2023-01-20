from ImageExtract import Area


def textTypeset(result, filename: str, img_areas: Area, h: int, w: int):
    txt = ""
    label = "%&%$\n"
    f = open(f'./output/{filename}.txt', 'a')
    if len(result) == 0:
        if len(img_areas):
            txt = txt + label
            f.write(txt)
            return
        else:
            return
    cut_h = int(h/9)
    cut_w = int(w/7)
    for idx in range(len(result)):
        coordinate = result[idx][0]
        x0 = int(min(coordinate[0][0], coordinate[3][0]))
        y0 = int(min(coordinate[0][1], coordinate[1][1]))
        x1 = int(max(coordinate[2][0], coordinate[1][0]))
        y1 = int(max(coordinate[2][1], coordinate[1][1]))
        x = (x0+x1)/2
        y = (y0+y1)/2
        if x < cut_w or x > w-cut_w or y < cut_h or y > h-cut_h:
            continue
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
