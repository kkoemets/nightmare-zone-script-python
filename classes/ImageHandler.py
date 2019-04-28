import logging

from classes.ImageBox import ImageBox

log = logging.getLogger("Mouse")

log.setLevel(logging.INFO)


class ImageHandler:

    @staticmethod
    def compare_cached_images(image1, image2):
        return ImageBox.are_equals(image1, image2)


    @staticmethod
    def get_image_out_of_location(location):
        bbox = ImageBox.get_bbox(
            location[0],
            location[1],
            location[2],
            location[3]
        )
        return ImageBox.image_grab_bbox(bbox)


    @staticmethod
    def get_bbox_out_of_4_points(x0, y0, x1, y1):
        return ImageBox.get_bbox(x0, y0, x1, y1)


    @staticmethod
    def get_image_out_of_bbox(bbox):
        return ImageBox.image_grab_bbox(bbox)
