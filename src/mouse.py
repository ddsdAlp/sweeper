import pyautogui
import time
from random import random, uniform
import config

# one-time helper to configure board coordinates
def configureCoords():
    print("Move cursor to the top-left of the board")
    time.sleep(5)
    x1, y1 = pyautogui.position()
    print("Top-left:", x1, y1)

    print("Move cursor to the bottom-right of the board")
    time.sleep(5)
    x2, y2 = pyautogui.position()
    print("Bottom-right:", x2, y2)

    print("Change the values in 'config.py' with the values below")
    print("Board Top:", y1)
    print("Board Left:", x1)
    print("Board Width:", x2 - x1)
    print("Board Height:", y2 - y1)

# human reaction time 150 - 300 ms
def waitRandom():
    chance = random()
    if(chance <= 0.05):
        t = uniform(2, 2.5)
    else:
        t = uniform(0.10, 0.35)
    time.sleep(t)

def offsetRandom():
    value = config.CELL_SIZE / 4
    o = uniform(-value, value)
    return o

def leftClickCell(row, col):
    CENTER_OFFSET = config.CELL_SIZE / 2
    top = config.BOARD_TOP + CENTER_OFFSET + offsetRandom()
    left = config.BOARD_LEFT + CENTER_OFFSET + offsetRandom()

    rowCoord = row * config.CELL_SIZE
    colCoord = col * config.CELL_SIZE

    # print(left + colCoord, top + rowCoord)

    waitRandom()
    pyautogui.moveTo(left + colCoord, top + rowCoord)
    pyautogui.click()

def rightClickCell(row, col):
    CENTER_OFFSET = config.CELL_SIZE / 2
    top = config.BOARD_TOP + CENTER_OFFSET + offsetRandom()
    left = config.BOARD_LEFT + CENTER_OFFSET + offsetRandom()

    rowCoord = row * config.CELL_SIZE
    colCoord = col * config.CELL_SIZE

    # print(left + colCoord, top + rowCoord)

    waitRandom()
    pyautogui.moveTo(left + colCoord, top + rowCoord)
    pyautogui.click(button='right')


