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

array_list_potions_enum = [Items.ITEM_ABSORPTION_POTION_4, Items.ITEM_ABSORPTION_POTION_3,
                           Items.ITEM_ABSORPTION_POTION_2, Items.ITEM_ABSORPTION_POTION_1]

absorption_potions = None
rock_cake_location = None
hp_1_location = None
opened_inventory_location = None
cached_opened_inventory_image = None
closed_inventory_location = None
cached_closed_inventory_image = None
cached_hp_1_image = None
cached_rock_cake_image = None


def main():  # Main method for the script, write code here
    global opened_inventory_location, cached_opened_inventory_image
    global closed_inventory_location, cached_closed_inventory_image
    global hp_1_location, cached_hp_1_image
    global absorption_potions
    global rock_cake_location, cached_rock_cake_image

    print('Welcome to Nightmare Zone Script')
    print('Requirements: ')
    print('1. Make sure you are in a dream with absorption potions')
    print('2. Rock Cake must be in the last row of inventory')
    print('3. With this version do not move/resize OSRS client window')
    print('4. All requirements above must be fulfilled to avoid a ban')
    input('Press enter to start...')

    log.info('Handling inventory')
    find_inventory_and_open_and_save_location_with_cache()

    log.info('Trying to find absorption potions')
    absorption_potions = get_absorption_potion_locations_and_doses()

    log.info('Drinking absorption potions until full')
    drink_absorptions_until_full(absorption_potions)

    log.info('Trying to find rock cake and guzzle it')
    find_and_guzzle_rock_cake()

    while get_doses_left(absorption_potions) > 0:
        Mouse.move_humanly_mouse_to_location(5, 5)
        Mouse.sleep_with_countdown(294413, 477855, 10000)  # 5 to 8 min approx 294413, 477855

        open_inventory_if_needed()

        log.info('Rediscovering absorption potions')
        absorption_potions = get_absorption_potion_locations_and_doses()
        log.info('Drinking absorptions until full')
        drink_absorptions_until_full(absorption_potions)

        log.info('Eating Rock Cake')
        rock_cake_image_to_check = Mouse.get_image_out_of_location(rock_cake_location)
        if not Mouse.compare_cached_images(cached_rock_cake_image, rock_cake_image_to_check):
            log.info('Handling inventory')
            find_inventory_and_open_and_save_location_with_cache()
            log.info('Trying to find rock cake and guzzle it')
            find_and_guzzle_rock_cake()
        else:
            guzzle_rock_cake_with_cached_hp_1(rock_cake_location, hp_1_location, cached_hp_1_image)

########################################################################################################################
def open_inventory_if_needed():
    global cached_closed_inventory_image, cached_opened_inventory_image
    global closed_inventory_location, opened_inventory_location

    opened_inv_img_to_check = Mouse.get_image_out_of_location(opened_inventory_location)
    if not Mouse.compare_cached_images(opened_inv_img_to_check, cached_opened_inventory_image):
        if closed_inventory_location is not None:
            closed_inv_img_to_check = Mouse.get_image_out_of_location(closed_inventory_location)
            if Mouse.compare_cached_images(closed_inv_img_to_check, cached_closed_inventory_image):
                Mouse.move_humanly_mouse_random_location_in_box(closed_inventory_location)
                Mouse.click(100)
            else:
                find_inventory_and_open_and_save_location_with_cache()
        else:
            find_inventory_and_open_and_save_location_with_cache()


def find_inventory_and_open_and_save_location_with_cache():
    global opened_inventory_location, cached_opened_inventory_image
    global closed_inventory_location, cached_closed_inventory_image

    log.info('Checking whether inventory is open')
    opened_inventory_location = get_location(PanelIcons.ICON_INVENTORY_SELECTED)
    if opened_inventory_location is None:
        log.info('Inventory is not open, opening')
        closed_inventory_location = get_location(PanelIcons.ICON_INVENTORY_UNSELECTED)
        cached_closed_inventory_image = Mouse.get_image_out_of_location(closed_inventory_location)
        Mouse.move_humanly_mouse_random_location_in_box(closed_inventory_location)
        Mouse.click(100)
        log.info('Opened inventory')

        # cursor will be on the image and thus will fail to find, moving away
        Mouse.move_humanly_mouse_to_location(5, 5)

        opened_inventory_location = get_location(PanelIcons.ICON_INVENTORY_SELECTED)
    log.debug('Saving opened inventory image to cache')
    cached_opened_inventory_image = Mouse.get_image_out_of_location(opened_inventory_location)


def find_and_guzzle_rock_cake():
    global rock_cake_location, cached_rock_cake_image
    global opened_inventory_location, cached_opened_inventory_image

    rock_cake_location = get_location(Items.ITEM_ROCK_CAKE)
    if rock_cake_location is None:
        sys.exit('Could not find rock cake, exiting script')
    cached_rock_cake_image = Mouse.get_image_out_of_location(rock_cake_location)
    log.info('Checking if need to guzzle rock cake')
    guzzle_rock_cake_uncached(cached_opened_inventory_image, opened_inventory_location, rock_cake_location)


def guzzle_rock_cake_uncached(cached_opened_inv_img, inv_loc, cake_loc):
    global hp_1_location, cached_hp_1_image

    i = 0  # fail-safe check
    while True:
        i += 1
        log.info('Checking whether hp is 1')
        hp_1_location = get_location(UI.UI_ICON_HP)
        if hp_1_location is None:
            log.info('HP is not 1, guzzling rock rake')
            if is_inventory_open(inv_loc, cached_opened_inv_img):
                guzzle_rock_cake(cake_loc, 13, 22)
            if i == 20:
                sys.exit('Something went wrong with guzzling rock cake!')
        else:
            cached_hp_1_image = Mouse.get_image_out_of_location(hp_1_location)
            break
    log.info('HP is 1')

def guzzle_rock_cake(location, min_times, max_times):
    log.info('Moving mouse to rock cake')
    random_location = location[0] + Mouse.get_rand_int(0, 16), location[1] + Mouse.get_rand_int(0, 1)
    Mouse.move_humanly_mouse_to_location(random_location[0], random_location[1])

    n = Mouse.get_rand_int(min_times, max_times)
    j = 0
    log.info('Guzzling')
    while j < n:
        Mouse.right_click()
        Mouse.click(100)
        Mouse.sleep(80, 120)
        j += 1


def guzzle_rock_cake_with_cached_hp_1(saved_rock_cake_location, hp_loc, cached_hp_image):
    random_location = saved_rock_cake_location[0] + Mouse.get_rand_int(0, 16), saved_rock_cake_location[
        1] + Mouse.get_rand_int(0, 1)
    Mouse.move_humanly_mouse_to_location(random_location[0], random_location[1])
    while not Mouse.are_images_equal(cached_hp_image, Mouse.get_image_out_of_location(hp_loc)):
        Mouse.right_click()
        Mouse.click(150)
        Mouse.sleep(80, 120)


def is_inventory_open(location, cached_inventory_image):
    image_of_inventory_location_state = Mouse.get_image_out_of_location(location)
    return Mouse.compare_cached_images(image_of_inventory_location_state, cached_inventory_image)


def drink_absorptions_until_full(pots_location_list):
    i = 0
    while i < len(pots_location_list):
        if pots_location_list[i].doses > 0:
            Mouse.move_humanly_mouse_random_location_in_box((
                pots_location_list[i].x,
                pots_location_list[i].y,
                pots_location_list[i].width,
                pots_location_list[i].height
            ))
            while pots_location_list[i].doses > 0:
                log.info('Drinking a dose of absorption potion')
                if not Mouse.click_and_sleep_and_return_if_change_occurred(30, 30, 732, 978):
                    return
                pots_location_list[i].doses -= 1
        i += 1
    return


def get_absorption_potion_locations_and_doses():
    abs_pot_list = []
    for item in array_list_potions_enum:
        for potion in Mouse.get_all_on_screen_as_list(item):
            doses = (int(str(item)[-1]))
            absorption_potion = AbsorptionPotion(potion[0], potion[1], potion[2], potion[3], doses)
            abs_pot_list.append(absorption_potion)
    # sorting by x, y coordinates
    abs_pot_list.sort(key=operator.itemgetter(0))
    abs_pot_list.sort(key=operator.itemgetter(1))
    return abs_pot_list


def get_location(saved_image_png):
    return Mouse.get_on_screen(saved_image_png)


def get_doses_left(potions):
    dose_counter = 0
    for potion in potions:
        dose_counter += potion.doses
    return dose_counter


main()
