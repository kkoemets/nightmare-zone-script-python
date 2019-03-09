import pyautogui
import time


while True:
    result = pyautogui.locateAllOnScreen('agility_obstacle_green.png')
    result = list(result)
    print(len(result))
    if result is not None:
        print()
        # pyautogui.moveTo(result[0], result[1])

    time.sleep(1)