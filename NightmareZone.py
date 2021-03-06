import logging
import operator
import sys

from classes.Potion import Potion
from classes.Mouse import Mouse
from enums.Items import Items
from enums.PanelIcons import PanelIcons
from enums.UI import UI

log = logging.getLogger("NightmareZone")
logging.info('Nightmare Zone Script')
log.setLevel(logging.DEBUG)

list_abs_potions_enum = [Items.ITEM_ABS_POTION_4, Items.ITEM_ABS_POTION_3,
                         Items.ITEM_ABS_POTION_2, Items.ITEM_ABS_POTION_1]

list_super_ranging_potions_enum = [Items.ITEM_SUPER_RANGING_POTION_4,
                                   Items.ITEM_SUPER_RANGING_POTION_3,
                                   Items.ITEM_SUPER_RANGING_POTION_2,
                                   Items.ITEM_SUPER_RANGING_POTION_1]

list_overload_potions_enum = [Items.ITEM_OVERLOAD_POTION_4,
                              Items.ITEM_OVERLOAD_POTION_3,
                              Items.ITEM_OVERLOAD_POTION_2,
                              Items.ITEM_OVERLOAD_POTION_1]


def main():  # Root
    print('Welcome to Nightmare Zone Script')
    print('Requirements: ')
    print('1. Make sure you are in a dream with absorption potions')
    print('2. Rock Cake must be in the last row of inventory')
    print('3. With this version do not move/resize OSRS client window')
    print('4. All requirements above must be fulfilled to avoid a ban')
    mode = ''
    while mode != '1' and mode != '2':
        mode = input('Type 1 for varying time mode, type 2 for overload mode (and press enter): ')
        print(mode)

    if mode is '1':
        super_ranging_mode()
    if mode is '2':
        overload_mode()


def overload_mode():
    do_drink_absorptions = True
    min_interval = 5.05
    max_interval = 5.1
    input('You need to have absorption potions, overloads and a rock cake in your inventory')
    input('Press enter to start...')
    while True:
        open_inventory_if_closed()

        absorption_potions = get_potion_doses_and_locations(list_abs_potions_enum, 0.985)
        abs_doses_left = get_doses_left(absorption_potions)

        if do_drink_absorptions:
            drink_absorptions_until_full(absorption_potions)

        do_drink_absorptions = do_drink_absorptions is False

        overload_potions = get_potion_doses_and_locations(list_overload_potions_enum, 0.985)
        overload_doses_before_drinking = get_doses_left(overload_potions)
        drink_a_dose_if_possible(overload_potions)
        Mouse.move_humanly_mouse_to_location(20, 20)

        after_drinking_doses = get_doses_left(get_potion_doses_and_locations(list_overload_potions_enum, 0.985))
        if overload_doses_before_drinking == after_drinking_doses:
            sys.exit('Did not drink a dose of overload potion, exiting script')

        Mouse.sleep_with_countdown(2395, 3542, 10000)

        find_and_guzzle_rock_cake()

        Mouse.move_humanly_mouse_to_location(20, 20)

        if not abs_doses_left > 0 or not overload_doses_before_drinking > 0:
            break
        else:
            temp_min_interval = int(min_interval * 60 * 1000)
            temp_max_interval = int(max_interval * 60 * 1000)
            Mouse.sleep_with_countdown(temp_min_interval, temp_max_interval, 40000)
    sys.exit('No more absorption potions left, exiting script!')


def super_ranging_mode():
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
        absorption_potions = get_potion_doses_and_locations(list_abs_potions_enum, 0.96)
        absorption_potions_doses_before_drinking = get_doses_left(absorption_potions)

        log.info('Drinking absorption potions until full')
        drink_absorptions_until_full(absorption_potions)

        if absorption_potions_doses_before_drinking == get_doses_left(
                get_potion_doses_and_locations(list_abs_potions_enum, 0.96)):
            sys.exit('Did not drink absorption potions, exiting script')

        log.info('Trying to find rock cake and guzzle it')
        find_and_guzzle_rock_cake()

        super_ranging_potions = get_potion_doses_and_locations(list_super_ranging_potions_enum,
                                                               0.96)
        log.debug('Drinking super ranging potion if there are any')
        drink_a_dose_if_possible(super_ranging_potions)

        Mouse.move_humanly_mouse_to_location(5, 5)

        if not get_doses_left(absorption_potions) > 0:
            break
        else:
            temp_min_interval = int(min_interval * 60 * 1000)
            temp_max_interval = int(max_interval * 60 * 1000)
            Mouse.sleep_with_countdown(temp_min_interval, temp_max_interval, 40000)
    sys.exit('No more absorption potions left, exiting script!')


def drink_a_dose_if_possible(potions_locations):
    if len(potions_locations) > 0:
        log.debug('Drinking a potion defined by mode')  # TODO good logging
        drink_dose(potions_locations)
    return potions_locations

def open_inventory_if_closed():
    inventory = Mouse.get_on_screen(PanelIcons.ICON_INVENTORY_SELECTED, 0.991)
    if inventory is None:
        inventory = Mouse.get_on_screen(PanelIcons.ICON_INVENTORY_UNSELECTED, 0.991)
        if inventory is None:
            sys.exit('Could not find inventory icon, exiting script')
        else:
            Mouse.move_humanly_mouse_random_location_in_box(inventory)
            Mouse.click(200)
            Mouse.sleep_with_countdown(400, 450, 450)


def find_and_guzzle_rock_cake():
    cake_location = Mouse.get_on_screen(Items.ITEM_ROCK_CAKE, 0.991)
    if cake_location is None:
        sys.exit('Could not find rock cake, exiting script')
    else:
        random_location = cake_location[0] + Mouse.get_rand_int(0, 16), cake_location[
            1] + Mouse.get_rand_int(0, 1)
        Mouse.move_humanly_mouse_to_location(random_location[0], random_location[1])
        guzzle_rock_cake_uncached()


def guzzle_rock_cake_uncached():
    i = 0  # fail-safe check
    while True:
        i += 1
        hp_1_location = Mouse.get_on_screen(UI.UI_ICON_HP, 0.995)
        if hp_1_location is None:
            log.info('Guzzling if hp is not 1')
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
                if not Mouse.click_and_sleep_and_return_if_change_occurred(30, 30, 332, 467):
                    return
                pots_location_list[i].doses -= 1
        i += 1
    return


def drink_dose(pots_location_list):
    Mouse.move_humanly_mouse_random_location_in_box((
        pots_location_list[0].x,
        pots_location_list[0].y,
        pots_location_list[0].width,
        pots_location_list[0].height
    ))
    Mouse.click(170)


def get_potion_doses_and_locations(potions_enum, confidence):
    abs_pot_list = []
    for item in potions_enum:
        for potion in Mouse.get_all_on_screen_as_list(item, confidence):
            doses = (int(str(item)[-1]))
            potions = Potion(potion[0], potion[1], potion[2], potion[3], doses)
            abs_pot_list.append(potions)
    # sorting by x, y coordinates
    abs_pot_list.sort(key=operator.itemgetter(0))
    abs_pot_list.sort(key=operator.itemgetter(1))
    return abs_pot_list


def get_doses_left(potions):
    dose_counter = 0
    for potion in potions:
        dose_counter += potion.doses
    return dose_counter


main()
