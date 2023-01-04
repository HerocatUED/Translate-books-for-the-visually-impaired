from scipy import ndimage
import numpy as np
import cv2


class Coordinate:
    def __init__(self, x0, x1, y0, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def __eq__(self, other) -> bool:
        return other.x0 == self.x0 and other.x1 == self.x1 and other.y0 == self.y0 and other.y1 == self.y1


# extract images and their coordinates from pages
def ImageSegment(pages):
    img_coordinates = []
    imgs = []
    for page in pages:
        page = ndimage.maximum_filter(page, 5)
        h, w = np.shape(page)
        threshold_h=int(h/100)
        threshold_w=int(w/100)
        coordinates_old = []
        coordinates_new = []
        coordinates_old.append(Coordinate(0, h, 0, w))
        while coordinates_old.len():
            for coordinate in coordinates_old:
                pass
    return img_coordinates, imgs
