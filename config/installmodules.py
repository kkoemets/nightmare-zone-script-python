from pip._internal import main
def install(package):
    main(['install', package])


try:
    import pyautogui
except ModuleNotFoundError:
    install('pyautogui')
try:
    import PIL
except ModuleNotFoundError:
    install('PIL')
try:
    import numpy
except ModuleNotFoundError:
    install('numpy')

try:
    import pyclick
except ModuleNotFoundError:
    install('pyclick')
try:
    import cv2
except ModuleNotFoundError:
    install('cv2')
    install('opencv-python')
