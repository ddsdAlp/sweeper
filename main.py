import mss
import pyautogui
import time
from dataclasses import dataclass, field

import mouse

@dataclass
class Tile:
    state: str
    bombGroupCount: int
    bombGroup: list = field(default_factory=list)

# MEDIUM BOARD - 16x16
BOARD_TOP = 493
BOARD_LEFT = 878
BOARD_WIDTH = 576
BOARD_HEIGHT = 576

ROWS, COLS = 16, 16
CELL_SIZE = BOARD_WIDTH // ROWS # 36
BOARD = [[Tile(state="-", bombGroupCount=0, bombGroup=[]) for i in range(COLS)] for j in range(ROWS)]

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
            temp = temp + str(BOARD[row][col].state) + " "
        print(temp)

# turn screenshot into BOARD array
def ssToArr(img):
    for row in range(ROWS):
        rowCoord = row * CELL_SIZE
        for col in range(COLS):
            colCoord = col * CELL_SIZE
            topLeftRGB = img.pixel(colCoord, rowCoord)
            typeCheckRGB = img.pixel(colCoord + 22, rowCoord + 26)

            # closed
            if topLeftRGB == (112, 120, 128):
                if typeCheckRGB in colorDict:
                    BOARD[row][col].state = colorDict[typeCheckRGB]
                else:
                    BOARD[row][col].state = "-"
            # opened
            elif topLeftRGB == (30, 38, 46):
                if typeCheckRGB in colorDict:
                    BOARD[row][col].state = colorDict[typeCheckRGB]
                else:
                    BOARD[row][col].state = "0"

    # printBoard()

# get all coords of neighbouring tiles
def getNeighbours(row, col):
    neighbours = []

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            if 0 <= row + i <= (16 - 1) and 0 <= col + j <= (16 - 1):
                neighbours.append((row + i, col + j))
    
    return neighbours

def checkTileCounts(neighbours):
    closedCount = 0
    flaggedCount = 0

    for i, j in neighbours:
        if BOARD[i][j].state == "-":
            closedCount += 1
        elif BOARD[i][j].state == "*":
            flaggedCount += 1
    
    return closedCount, flaggedCount

# =========== Action Functions ===========

def openClosedNeighbours(neighbours):
    for i, j in neighbours:
        if BOARD[i][j].state == "-":
            BOARD[i][j].state = "-1"
            mouse.leftClickCell(i, j)

def flagClosedNeighbours(neighbours):
    for i, j in neighbours:
        if BOARD[i][j].state == "-":
            BOARD[i][j].state = "*"
            mouse.rightClickCell(i, j)

# ========================================

def processBoard():
    for row in range(ROWS):
        for col in range(COLS):
            tile = BOARD[row][col]

            # skip unnecessarry tiles
            if tile.state in ["-", "0", "*"]:
                continue
            
            # get all neighbour coords
            neighbours = getNeighbours(row, col)

            # number of closed and flagged neighbours
            closed, flagged = checkTileCounts(neighbours)

            if int(tile.state) == closed + flagged:
                flagClosedNeighbours(neighbours)
            
            if int(tile.state) == flagged:
                openClosedNeighbours(neighbours)                 

# take screenshot of the board
with mss.mss() as sct:
    # The screen part to capture
    monitor = {"top": BOARD_TOP, "left": BOARD_LEFT, "width": BOARD_WIDTH, "height": BOARD_HEIGHT}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)
    ssToArr(sct_img)
    
    loop = 0
    while loop < 10:
        loop += 1

        processBoard()

        sct_img = sct.grab(monitor)
        ssToArr(sct_img)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)