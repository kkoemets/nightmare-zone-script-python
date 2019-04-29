import logging
import time
from random import randint

import pyautogui
from pyclick import HumanClicker
import cv2

from classes.Box import Box
from classes.ImageHandler import ImageHandler

log = logging.getLogger("Mouse")

log.setLevel(logging.INFO)

class Mouse:

    @staticmethod
    def get_rand_int(min_int, max_int):
        return randint(min_int, max_int)


    @staticmethod
    def click_and_sleep_and_return_if_change_occurred(width, height, sleep_time_min_milliseconds,
                                                      sleep_time_max_milliseconds):
        x = pyautogui.position().x
        y = pyautogui.position().y
        sleep_time = randint(sleep_time_min_milliseconds, sleep_time_max_milliseconds)

        bbox_to_compare = ImageHandler.get_bbox_out_of_4_points(x - width, y - height, width * 2, height * 2)
        im_before = ImageHandler.get_image_out_of_bbox(bbox_to_compare)
        log.debug('Created image grab before sleep')

        pyautogui.click()

        time.sleep(sleep_time/1000)

        im_after = ImageHandler.get_image_out_of_bbox(bbox_to_compare)
        log.debug('Created image grab after sleep')

        i = 0
        while i < 20 and ImageHandler.compare_cached_images(im_before, im_after):
            im_after = ImageHandler.get_image_out_of_bbox(bbox_to_compare)
            sleep = randint(20, 61)
            time.sleep(sleep / 1000)
            i += 1

        return not ImageHandler.compare_cached_images(im_before, im_after)


    @staticmethod
    def sleep_with_countdown(sleep_time_min_milliseconds, sleep_time_max_milliseconds, countdown_interval_milliseconds):
        sleep_time = randint(sleep_time_min_milliseconds, sleep_time_max_milliseconds)
        while sleep_time > 0:
            if sleep_time >= countdown_interval_milliseconds:
                log.info(str(round(sleep_time / 1000 / 60, 2)) + ' minutes left to sleep')
                sleep_time -= countdown_interval_milliseconds
                time.sleep(countdown_interval_milliseconds / 1000)
            else:
                log.info('Will end in ' + str(round(sleep_time / 1000 / 60, 2)) + ' seconds')
                time.sleep(sleep_time / 1000)
                break


    @staticmethod
    def click(sleep_time_milliseconds):
        time.sleep(sleep_time_milliseconds / 1000)
        pyautogui.click()


    @staticmethod
    def get_all_on_screen_as_list(item, confidence):
        items = list(pyautogui.locateAllOnScreen(item.value, confidence=confidence))
        log.info(str(item) + ' : ' + str(len(items)) + ' on screen')
        return items


    @staticmethod
    def get_on_screen(item, confidence):
        target = pyautogui.locateOnScreen(item.value, confidence=confidence)
        if target is not None:
            log.info('Found ' + str(item) + ' on screen')
        else:
            log.info('Unable to find ' + str(item) + ' on screen')
        return target


    @staticmethod
    def move_humanly_mouse_random_location_in_box(box):
        hc = HumanClicker()
        box = Box(box)
        delta_x = randint(0, box.width())
        delta_y = randint(0, box.height())
        to_location = (int(box.x() + delta_x), int(box.y() + delta_y))
        hc.move(to_location, 0.5)


    @staticmethod
    def move_humanly_mouse_to_location(x, y):
        hc = HumanClicker()
        hc.move((int(x), int(y)), 0.5)


    @staticmethod
    def right_click():
        pyautogui.rightClick()

