import pyautogui

from enum import Enum
import logging
from random import randint

log = logging.getLogger("Main")
log.setLevel(logging.DEBUG)


class Items(Enum):
    ITEM_ABSORPTION_POTION_4 = './images/item_absorption_potion_4.PNG'


def move_mouse_middle(box):
    pyautogui.click(box[0] + box[2] / 2, box[1] + box[3] / 2)


def move_mouse_to_random_location_in_box(box):
    x_delta = randint(0, box[2])
    y_delta = randint(0, box[3])
    x = box[0] + x_delta
    y = box[1] + y_delta
    pyautogui.click(x, y)




# logging.info('Starting Nightmare Zone Bot')
#
# log.info('Counting absorption potions')
#
# ITEM_ABSORPTION_4 = './images/item_absorption_potion_4.PNG'
#
# while True:
#     array_absorption_potions = list(pyautogui.locateAllOnScreen(ITEM_ABSORPTION_4))
#     log.debug('Full absorption potions: ')
#

