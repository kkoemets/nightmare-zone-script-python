import logging
import operator
import sys

from classes.AbsorptionPotion import AbsorptionPotion
from classes.Mouse import Mouse
from enums.Items import Items
from enums.PanelIcons import PanelIcons
from enums.UI import UI

log = logging.getLogger("NightmareZone")
logging.info('Nightmare Zone Script')
log.setLevel(logging.DEBUG)

array_list_potions_enum = [Items.ITEM_ABSORPTION_POTION_4,
                           Items.ITEM_ABSORPTION_POTION_3,
                           Items.ITEM_ABSORPTION_POTION_2,
                           Items.ITEM_ABSORPTION_POTION_1,
                           ]

absorption_potions_list = []
temp_delay = 500  # temporary, used for constant timing between clicks
rock_cake_location = []
hp_ui_location = []  # will be used to check whether something has happened to client


def main():  # Main method for the script, write code here
    print('Welcome to Nightmare Zone Script')
    print('Requirements: ')
    print('1. Make sure you are in a dream with absorption potions')
    print('2. Rock Cake must be in the last row of inventory')
    print('3. With this version do not move/resize OSRS client window')
    print('4. All requirements above must be fulfilled to avoid a ban')
    input('Press enter to start...')

    log.info('Script is searching for stuff in client')
    log.info('Trying to find absorption potions')
    open_inventory_and_save_potion_locations_and_doses()

    log.info('Trying to find Rock Cake')
    global rock_cake_location
    rock_cake_location = open_inventory_and_get_rock_cake_box()

    log.info('Script has found everything')

    log.info('Drinking absorption potions until full')
    open_inventory_and_drink_absorptions_full()

    log.info('Checking whether HP is 1')
    i = 0
    while not is_hp_one():
        i += 1
        log.info('HP is not 1, eating Rock Cake')
        open_inventory_and_guzzle_rock_cake()
        if i == 20:
            sys.exit('Something went wrong with guzzling rock cake!')

    log.info('HP is 1')
    log.debug('Saving image from location where HP is shown 1, will be faster to check from now on')
    image_hp = Mouse.get_image_of_box(hp_ui_location[0][0],
                                      hp_ui_location[0][1],
                                      hp_ui_location[0][2],
                                      hp_ui_location[0][3]
                                      )
    while get_doses_left() > 0:
        Mouse.sleep_with_countdown(294413, 477855, 10000)  # 5 to 8 min approx 294413, 477855

        open_inventory_and_save_potion_locations_and_doses()
        log.info('Drinking absorptions until full')
        open_inventory_and_drink_absorptions_full()

        log.info('Eating Rock Cake')
        rock_cake_location_to_check = open_inventory_and_get_rock_cake_box()
        if rock_cake_location != rock_cake_location_to_check:
            rock_cake_location = rock_cake_location_to_check
            i = 0
            while not is_hp_one():
                i += 1
                log.info('HP is not 1, eating Rock Cake')
                open_inventory_and_guzzle_rock_cake()
                if i == 20:
                    sys.exit('Something went wrong with guzzling rock cake!')
            image_hp = Mouse.get_image_of_box(hp_ui_location[0][0],
                                              hp_ui_location[0][1],
                                              hp_ui_location[0][2],
                                              hp_ui_location[0][3]
                                              )
        else:
            open_inventory_and_guzzle_until_hp_is_1(image_hp)
########################################################################################################################

def is_hp_one():
    hp_ui_location.clear()
    temp = Mouse.get_on_screen(UI.UI_ICON_HP)
    if temp is not None:
        hp_ui_location.append(temp)
    return temp is not None


def open_inventory_and_get_rock_cake_box():
    while not is_inventory_open():
        open_inventory(temp_delay)

    location = Mouse.get_on_screen(Items.ITEM_ROCK_CAKE)

    if location is not None:
        return location
    else:
        sys.exit('Could not find inventory icon, exiting script')


def open_inventory_and_guzzle_until_hp_is_1(saved_im):
    open_inventory(temp_delay)

    random_rock_cake_location = \
        rock_cake_location[0] + Mouse.get_rand_int(0, 16), \
        rock_cake_location[1] + Mouse.get_rand_int(0, 1)
    log.debug('Rock Cake location box ' + str(rock_cake_location))
    log.debug('Pixel to be clicked on Rock cake ' + str(random_rock_cake_location))
    Mouse.move_mouse_to_location(
        random_rock_cake_location[0],
        random_rock_cake_location[1]
    )
    while not Mouse.are_images_equal(saved_im,
                                     Mouse.get_image_of_box(hp_ui_location[0][0],
                                                            hp_ui_location[0][1],
                                                            hp_ui_location[0][2],
                                                            hp_ui_location[0][3])):
        Mouse.right_click()
        Mouse.click(200)
        Mouse.sleep(89, 156)


def open_inventory_and_guzzle_rock_cake():
    open_inventory(temp_delay)
    log.info(rock_cake_location)

    random_rock_cake_location = \
        rock_cake_location[0] + Mouse.get_rand_int(0, 16), \
        rock_cake_location[1] + Mouse.get_rand_int(0, 1)
    Mouse.move_mouse_to_location(
        random_rock_cake_location[0],
        random_rock_cake_location[1]
    )
    i = 0

    while i < Mouse.get_rand_int(7, 14):
        Mouse.right_click()
        Mouse.click(200)
        Mouse.sleep(89, 156)
        i += 1


def open_inventory_and_drink_absorptions_full():
    open_inventory(temp_delay)

    i = 0
    while i < len(absorption_potions_list):
        if absorption_potions_list[i].doses > 0:
            Mouse.move_mouse_random_location_in_box((
                absorption_potions_list[i].x,
                absorption_potions_list[i].y,
                absorption_potions_list[i].width,
                absorption_potions_list[i].height
            ))
            while absorption_potions_list[i].doses > 0:
                if not Mouse.click_and_sleep_and_return_if_change_occurred(30, 30, 732, 978):
                    return
                absorption_potions_list[i].doses -= 1
        i += 1
    return


def open_inventory_and_save_potion_locations_and_doses():
    open_inventory(temp_delay)
    global absorption_potions_list
    absorption_potions_list = []
    for item in array_list_potions_enum:
        for potion in Mouse.get_all_on_screen_as_list(item):
            doses = (int(str(item)[-1]))
            absorption_potion = AbsorptionPotion(potion[0], potion[1], potion[2], potion[3], doses)
            absorption_potions_list.append(absorption_potion)
    # sorting by x, y coordinates
    absorption_potions_list.sort(key=operator.itemgetter(0))
    absorption_potions_list.sort(key=operator.itemgetter(1))

def is_inventory_open():
    result = Mouse.get_on_screen(PanelIcons.ICON_INVENTORY_SELECTED)
    return result is not None


def open_inventory(sleep_time_milliseconds):
    if not is_inventory_open():
        inventory_location_unselected = Mouse.get_on_screen(PanelIcons.ICON_INVENTORY_UNSELECTED)
        if inventory_location_unselected is not None:
            log.info('Opening inventory')
            Mouse.move_mouse_random_location_in_box(inventory_location_unselected)
            Mouse.click(sleep_time_milliseconds)
            Mouse.sleep(100, 150)  # hack for bug fix
        else:
            sys.exit('Could not find inventory icon, exiting script')


def get_doses_left():
    dose_counter = 0
    for potion in absorption_potions_list:
        dose_counter += potion.doses
    return dose_counter


main()
