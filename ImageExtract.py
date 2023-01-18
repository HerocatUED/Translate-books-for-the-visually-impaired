import cv2
import sys
import random
import numpy as np
from scipy import ndimage
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
    gray_page = ndimage.gaussian_filter(spread_page, 20, mode='reflect')
    h, w = np.shape(gray_page)
    # hard-code parameter: sample_w, sample_h, stride
    sample_w = 7
    sample_h = 9
    stride = 100
    img_threshold = 240
    grid_w = w/(sample_w+1)
    grid_h = h/(sample_h+1)
    visited = np.zeros([int(h/stride), int(h/stride)], dtype=np.int8)
    # sample points and spread
    for i in range(1, sample_w+1):
        for j in range(1, sample_h+1):
            tx = int(grid_w*i)
            ty = int(grid_h*j)
            if gray_page[ty][tx] >= img_threshold:
                continue
            flag = False
            if len(areas):
                for area in areas:
                    if area.contain(tx, ty):
                        flag = True
                        break
            if flag:
                continue
            img_area = Area(tx, tx, ty, ty)
            visited[int(ty/stride)][int(tx/stride)] = 1
            spread(tx, ty, w, h, stride, visited,
                   gray_page, img_area, img_threshold)
            contain_flag = False
            for i in range(len(areas)):
                area = areas[i]
                if img_area.contain(int((area.x0+area.x1)/2), int((area.y0+area.y1)/2)):
                    contain_flag = True
                    areas[i] = img_area
                    break
            if not contain_flag:
                areas.append(img_area)
    areas.sort()
    for area in areas:
        if (area.x1-area.x0)*(area.y1-area.y0) < h*w/45:
            continue
        pictures.append(area.cut(masked_page))
    if len(textBox) == 0:
        if len(areas):
            return [Area(0, 0, 0, 0)], [page]
        else:
            return [], []

    return areas, pictures


dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]


def spread(x: int, y: int, w: int, h: int, stride: int, visited,  gray_page, area: Area, img_threshold: int):
    d = int(stride/10)
    delta1 = random.randint(-d, d)
    delta2 = random.randint(-d, d)
    for i in range(4):
        new_x = int(x+dx[i]*stride)+delta1
        new_y = int(y+dy[i]*stride)+delta2
        visit_x = int(new_x/stride)
        visit_y = int(new_y/stride)
        if new_x >= 0 and new_x < w and new_y >= 0 and new_y < h and (not visited[visit_y][visit_x]) and gray_page[new_y][new_x] < img_threshold:
            area.update(new_x, new_y)
            visited[visit_y][visit_x] = 1
            spread(new_x, new_y, w, h, stride, visited,
                   gray_page, area, img_threshold)
        else:
            try_x = int(x+dx[i]*stride/2)
            try_y = int(y+dy[i]*stride/2)
            visit_x = int(try_x/stride)
            visit_y = int(try_y/stride)
            if try_x >= 0 and try_x < w and try_y >= 0 and try_y < h and (not visited[visit_y][visit_x]) and gray_page[try_y][try_x] < img_threshold:
                area.update(try_x, try_y)
                visited[visit_y][visit_x] = 1
                spread(try_x, try_y, w, h, stride, visited,
                       gray_page, area, img_threshold)


def mask(page, textBox):
    for text in textBox:
        coordinate = text[0]
        x0 = int(min(coordinate[0][0], coordinate[3][0]))-5
        y0 = int(min(coordinate[0][1], coordinate[1][1]))-5
        x1 = int(max(coordinate[2][0], coordinate[1][0]))+5
        y1 = int(max(coordinate[2][1], coordinate[1][1]))+5
        for i in range(3):
            color_sum = 0
            color_sum += np.sum(page[y0:y1+1, x0, i])
            color_sum += np.sum(page[y0:y1+1, x1, i])
            color_sum += np.sum(page[y0, x0+1:x1, i])
            color_sum += np.sum(page[y1, x0+1:x1, i])
            color = color_sum/(y1-y0+x1-x0+2)/2
            page[y0:y1+1, x0:x1+1, i] = color
        # page[y0-5:y1+6, x0-5:x1+6, :] = 255
    return page

