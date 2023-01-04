from scipy import ndimage, spatial
import numpy as np
import cv2


# extract images and their coordinates from pages
def ImageSegment(img):
    coordinates=[]
    imgs=[]
    return coordinates,imgs