import logging
import time
from random import randint

import pyautogui
from pyclick import HumanClicker

from classes.Box import Box
from classes.ImageBox import ImageBox

log = logging.getLogger("Mouse")

log.setLevel(logging.DEBUG)


class Mouse:

    @staticmethod
    def are_images_equal(im_0, im_1):
        return ImageBox.are_equals(im_0, im_1)

    @staticmethod
    def get_image_of_box(x, y, width, height):
        bbox = ImageBox.get_bbox(x, y, width, height)
        return ImageBox.image_grab_bbox(bbox)

    @staticmethod
    def click_and_sleep_and_return_if_change_occurred(width, height, sleep_time_min_milliseconds,
                                                      sleep_time_max_milliseconds):
        x = pyautogui.position().x
        y = pyautogui.position().y
        bbox = ImageBox.get_bbox(x, y, width, height)
        sleep_time = randint(sleep_time_min_milliseconds, sleep_time_max_milliseconds)

        im_before = ImageBox.image_grab_bbox(bbox)
        log.debug('Created image grab before sleep')
        log.debug(im_before)

        pyautogui.click()

        time.sleep(sleep_time/1000)

        im_after = ImageBox.image_grab_bbox(bbox)
        log.debug('Created image grab after sleep')
        log.debug(im_after)
        if not ImageBox.are_equals(im_before, im_after):
            time.sleep(300 / 1000)
            im_after = ImageBox.image_grab_bbox(bbox_to_compare)

        return not ImageBox.are_equals(im_before, im_after)

    @staticmethod
    def sleep(sleep_time_min_milliseconds, sleep_time_max_milliseconds):
        sleep_time = randint(sleep_time_min_milliseconds, sleep_time_max_milliseconds)
        log.info('Sleeping for ' + str(sleep_time) + ' milliseconds'),
        time.sleep(sleep_time / 1000)

    def sleep_with_countdown(sleep_time_min_milliseconds, sleep_time_max_milliseconds, countdown_interval_milliseconds):
        sleep_time = randint(sleep_time_min_milliseconds, sleep_time_max_milliseconds)
        while sleep_time > 0:
            if sleep_time >= countdown_interval_milliseconds:
                log.info(str(sleep_time / 1000 / 60) + ' minutes left to sleep')
                sleep_time -= countdown_interval_milliseconds
                time.sleep(countdown_interval_milliseconds / 1000)
            else:
                log.info('Will end in ' + str(sleep_time / 1000 / 60) + ' seconds')
                time.sleep(sleep_time / 1000)
                break


    @staticmethod
    def click(sleep_time_milliseconds):
        time.sleep(sleep_time_milliseconds / 1000)
        pyautogui.click()

    @staticmethod
    def get_all_on_screen_as_list(item):
        """
        Returns all instances of a image on screen as list
        :param item:
        :return:
        """
        items = list(pyautogui.locateAllOnScreen(item.value))
        log.debug(str(item) + ' : ' + str(len(items)) + ' on screen')
        return items

    @staticmethod
    def get_on_screen(item):
        target = pyautogui.locateOnScreen(item.value)
        if target is not None:
            log.debug('Found ' + str(item) + ' on screen')
        else:
            log.debug('Unable to find ' + str(item) + ' on screen')
        return target

    @staticmethod
    def move_mouse_random_location_in_box(box):
        hc = HumanClicker()
        box = Box(box)
        delta_x = randint(0, box.width())
        delta_y = randint(0, box.height())
        hc.move((box.x() + delta_x, box.y() + delta_y), 0.5)

    # todo look ..._location_in_box
    @staticmethod
    def move_mouse_to_location(x, y):
        hc = HumanClicker()
        hc.move((x, y), 0.5)

    @staticmethod
    def get_rand_int(min_int, max_int):
        return randint(min_int, max_int)

    @staticmethod
    def right_click():
        pyautogui.rightClick()
