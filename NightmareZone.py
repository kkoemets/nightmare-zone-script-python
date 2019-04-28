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


def main():  # Main method for the script, write code here
    print('Welcome to Nightmare Zone Script')
    print('Requirements: ')
    print('1. Make sure you are in a dream with absorption potions')
    print('2. Rock Cake must be in the last row of inventory')
    print('3. With this version do not move/resize OSRS client window')
    print('4. All requirements above must be fulfilled to avoid a ban')
    min_interval = input('Enter minimum time in minutes to sleep (minimum 2 min): ')
    max_interval = input('Enter maximum time in minutes to sleep (maximum 19 min): ')
    try:
        min_interval = float(min_interval)
        max_interval = float(max_interval)
    except ValueError:
        sys.exit('Sleep min/max time was not a number!')
    if min_interval < 2 or max_interval > 19 or min_interval >= max_interval:
        sys.exit('Sleep times were not correct!')
    input('Press enter to start...')

    while True:
        open_inventory_if_closed()

        log.info('Trying to find absorption potions')
        absorption_potions = get_absorption_potion_locations_and_doses()

        log.info('Drinking absorption potions until full')
        drink_absorptions_until_full(absorption_potions)

        log.info('Trying to find rock cake and guzzle it')
        find_and_guzzle_rock_cake()
        Mouse.move_humanly_mouse_to_location(5, 5)
        if not get_doses_left(absorption_potions) > 0:
            break

        temp_min_interval = int(min_interval * 60 * 1000)
        temp_max_interval = int(max_interval * 60 * 1000)
        Mouse.sleep_with_countdown(temp_min_interval, temp_max_interval, 10000)

########################################################################################################################
def open_inventory_if_closed():
    inventory = Mouse.get_on_screen(PanelIcons.ICON_INVENTORY_SELECTED)
    if inventory is None:
        inventory = Mouse.get_on_screen(PanelIcons.ICON_INVENTORY_UNSELECTED)
        if inventory is None:
            sys.exit('Could not find inventory icon, exiting script')
        else:
            Mouse.move_humanly_mouse_random_location_in_box(inventory)
            Mouse.click(200)


def find_and_guzzle_rock_cake():
    cake_location = Mouse.get_on_screen(Items.ITEM_ROCK_CAKE)
    if cake_location is None:
        sys.exit('Could not find rock cake, exiting script')
    else:
        random_location = cake_location[0] + Mouse.get_rand_int(0, 16), cake_location[1] + Mouse.get_rand_int(0, 1)
        Mouse.move_humanly_mouse_to_location(random_location[0], random_location[1])
        guzzle_rock_cake_uncached()


def guzzle_rock_cake_uncached():
    i = 0  # fail-safe check
    while True:
        i += 1
        log.info('Checking whether hp is 1')
        hp_1_location = get_location(UI.UI_ICON_HP)
        if hp_1_location is None:
            log.info('HP is not 1, guzzling rock rake')
            guzzle_rock_cake()
            if i == 50:
                sys.exit('Something went wrong with guzzling rock cake!')
        else:
            break
    log.info('HP is 1')


def guzzle_rock_cake():
    Mouse.right_click()
    sleep = Mouse.get_rand_int(67, 133)
    Mouse.click(sleep)


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
                if not Mouse.click_and_sleep_and_return_if_change_occurred(30, 30, 587, 734):
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
