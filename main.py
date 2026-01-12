import mss
import pyautogui
import time

# MEDIUM BOARD - 16x16
BOARD_TOP = 493
BOARD_LEFT = 878
BOARD_WIDTH = 576
BOARD_HEIGHT = 576

ROWS, COLS = 16, 16
CELL_SIZE = BOARD_WIDTH // ROWS # 36
print(CELL_SIZE)

colorDict = {
    (112, 120, 128) : "closed",
    (30, 38, 46) : "opened",
    (216, 224, 232) : "*", # flag
    (124, 199, 255) : "1",
    (102, 194, 102) : "2",
    (255, 119, 136) : "3",
    (238, 136, 255) : "4",
    (221, 170, 34)  : "5",
    (102, 204, 204) : "6",
}

# Problematic Initialization:
# BOARD = [["-"] * COLS] * ROWS
# Correct Initialization:
BOARD = [["-" for i in range(COLS)] for j in range(ROWS)]

# Configure board coordinates
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

# print the BOARD array
def printBoard():
    for row in range(ROWS):
        temp = ""
        for col in range(COLS):
            temp = temp + str(BOARD[row][col]) + " "
        print(temp)

# turn screenshot into BOARD array
def processBoard(img):
    for row in range(ROWS):
        rowCoord = row * CELL_SIZE
        for col in range(COLS):
            colCoord = col * CELL_SIZE
            topLeftRGB = img.pixel(colCoord, rowCoord)
            typeCheckRGB = img.pixel(colCoord + 22, rowCoord + 26)

            # closed
            if topLeftRGB == (112, 120, 128):
                if typeCheckRGB in colorDict:
                    BOARD[row][col] = colorDict[typeCheckRGB]
                else:
                    BOARD[row][col] = "-"
            # opened
            elif topLeftRGB == (30, 38, 46):
                if typeCheckRGB in colorDict:
                    BOARD[row][col] = colorDict[typeCheckRGB]
                else:
                    BOARD[row][col] = "0"

    printBoard()

# take screenshot of the board
with mss.mss() as sct:
    # The screen part to capture
    monitor = {"top": BOARD_TOP, "left": BOARD_LEFT, "width": BOARD_WIDTH, "height": BOARD_HEIGHT}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)
    processBoard(sct_img)
    
    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)