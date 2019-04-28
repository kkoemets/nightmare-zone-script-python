import logging

from PIL import Image
from PIL import ImageGrab
import numpy as np


log = logging.getLogger("ImageBox")

log.setLevel(logging.INFO)

class ImageBox:

    @staticmethod
    def are_equals(im_0, im_1):
        arr0 = np.array(im_0)
        arr1 = np.array(im_1)

        if arr0.shape != arr1.shape:
            return False

        are_same = np.max(np.abs(arr0 - arr1)) == 0
        log.debug(are_same)
        return are_same

    @staticmethod
    def image_grab_bbox(bbox):
        image_grab = ImageGrab.grab(bbox=bbox)     # bbox=(a,b,c,d)
        return image_grab

    @staticmethod
    def get_bbox(x, y, width, height):
        log.debug('x:' + str(x) + ' y:' + str(y))
        return x, y, x + width, y + height
