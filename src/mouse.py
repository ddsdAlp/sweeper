import pyautogui
import time

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

def leftClickCell(row, col):
    CENTER_OFFSET = 18
    BOARD_TOP = 493 + CENTER_OFFSET
    BOARD_LEFT = 878 + CENTER_OFFSET

    rowCoord = row * 36
    colCoord = col * 36

    pyautogui.moveTo(BOARD_LEFT + colCoord, BOARD_TOP + rowCoord)
    pyautogui.click()

def rightClickCell(row, col):
    CENTER_OFFSET = 18
    BOARD_TOP = 493 + CENTER_OFFSET
    BOARD_LEFT = 878 + CENTER_OFFSET

    rowCoord = row * 36
    colCoord = col * 36

    pyautogui.moveTo(BOARD_LEFT + colCoord, BOARD_TOP + rowCoord)
    pyautogui.click(button='right')


