import pyautogui

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


