import pyautogui
import time
from random import random, uniform

# one-time helper to configure board coordinates
def configureCoords():
    print("move to top-left of board")
    time.sleep(5)
    x1, y1 = pyautogui.position()
    print("Top-left:", x1, y1)

    print("move to bottom-right of board")
    time.sleep(5)
    x2, y2 = pyautogui.position()
    print("Bottom-right:", x2, y2)

    print("Width:", x2 - x1)
    print("Height:", y2 - y1)

# human reaction time 150 - 300 ms
def waitRandom():
    chance = random()
    if(chance <= 0.05):
        t = uniform(2, 2.5)
    else:
        t = uniform(0.10, 0.35)
    time.sleep(t)

def offsetRandom():
    o = uniform(-8, 8)
    return o

def leftClickCell(row, col):
    CENTER_OFFSET = 18
    BOARD_TOP = 493 + CENTER_OFFSET + offsetRandom()
    BOARD_LEFT = 878 + CENTER_OFFSET + offsetRandom()

    rowCoord = row * 36
    colCoord = col * 36

    waitRandom()
    pyautogui.moveTo(BOARD_LEFT + colCoord, BOARD_TOP + rowCoord)
    pyautogui.click()

def rightClickCell(row, col):
    CENTER_OFFSET = 18
    BOARD_TOP = 493 + CENTER_OFFSET + offsetRandom()
    BOARD_LEFT = 878 + CENTER_OFFSET + offsetRandom()

    rowCoord = row * 36
    colCoord = col * 36

    waitRandom()
    pyautogui.moveTo(BOARD_LEFT + colCoord, BOARD_TOP + rowCoord)
    pyautogui.click(button='right')


