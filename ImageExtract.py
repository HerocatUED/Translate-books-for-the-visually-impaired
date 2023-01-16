from scipy import ndimage
import numpy as np
import cv2
import sys
sys.setrecursionlimit(2000)


class Area:  # x-width / y-height
    def __init__(self, x0: int, x1: int, y0: int, y1: int):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def __eq__(self, other) -> bool:
        return other.x0 == self.x0 and other.x1 == self.x1 and other.y0 == self.y0 and other.y1 == self.y1

    def __lt__(self, other) -> bool:
        return self.y1 < other.y1

    def update(self, x: int, y: int):
        self.x0 = min(self.x0, x)
        self.x1 = max(self.x1, x)
        self.y0 = min(self.y0, y)
        self.y1 = max(self.y1, y)

    def contain(self, x: int, y: int) -> bool:
        return x >= self.x0 and x <= self.x1 and y >= self.y0 and y <= self.y1

    def cut(self, page):
        return page[self.y0:self.y1+1, self.x0:self.x1+1, :]


# extract images and their areas from pages
def ImageExtractor(page, textBox):
    areas = []  # [page: area1,area2,...]
    pictures = []  # [img1,img2,img3, ...]
    masked_page = mask(page, textBox)  # mask characters
    spread_page = cv2.cvtColor(masked_page, cv2.COLOR_BGR2GRAY)  # gray-scale
    h, w = np.shape(spread_page)
    # hard-code parameter: sample_w, sample_h, stride
    sample_w = 5
    sample_h = 7
    stride = 100
    grid_w = w/(sample_w+1)
    grid_h = h/(sample_h+1)
    visited = np.zeros([h, w], dtype=np.int8)
    # sample points and spread
    for i in range(1, sample_w+1):
        for j in range(1, sample_h+1):
            tx = int(grid_w*i)
            ty = int(grid_h*j)
            if spread_page[ty][tx] >= 240:
                continue
            flag = False
            if len(areas):
                for area in areas:
                    if(area.contain(tx, ty)):
                        flag = True
                        break
            if flag:
                continue
            img_area = Area(tx, tx, ty, ty)
            visited[ty][tx] = 1
            spread(tx, ty, w, h, stride, visited, spread_page, img_area)
            areas.append(img_area)
    areas.sort()
    for area in areas:
        if (area.x1-area.x0)*(area.y1-area.y0) < h*w/200:
            continue
        pictures.append(area.cut(masked_page))
    return areas, pictures


dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]


def spread(x: int, y: int, w: int, h: int, stride: int, visited, spread_page, area: Area):
    for i in range(4):
        new_x = int(x+dx[i]*stride)
        new_y = int(y+dy[i]*stride)
        if new_x >= 0 and new_x < w and new_y >= 0 and new_y < h and (not visited[new_y][new_x]) and spread_page[new_y][new_x] < 240:
            area.update(new_x, new_y)
            visited[new_y][new_x] = 1
            spread(new_x, new_y, w, h, stride, visited, spread_page, area)
        else:
            try_x = int(x+dx[i]*stride/2)
            try_y = int(y+dy[i]*stride/2)
            if try_x >= 0 and try_x < w and try_y >= 0 and try_y < h and (not visited[try_y][try_x]) and spread_page[try_y][try_x] < 240:
                area.update(try_x, try_y)
                visited[try_y][try_x] = 1
                spread(try_x, try_y, w, h, stride, visited, spread_page, area)


def mask(page, textBox):
    for text in textBox:
        coordinate = text[0]
        x0 = int(coordinate[0][0])
        y0 = int(coordinate[0][1])
        x1 = int(coordinate[2][0])
        y1 = int(coordinate[2][1])
        for i in range(3):
            color_sum = 0
            color_sum += np.sum(page[y0:y1+1, x0, i])
            color_sum += np.sum(page[y0:y1+1, x1, i])
            color_sum += np.sum(page[y0, x0+1:x1, i])
            color_sum += np.sum(page[y1, x0+1:x1, i])
            color = color_sum/(y1-y0+x1-x0+2)/2
            page[y0-5:y1+6, x0-5:x1+6, i] = color
    return page
