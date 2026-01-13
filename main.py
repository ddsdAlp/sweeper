import mss
import pyautogui
import time
from dataclasses import dataclass, field

import mouse

log = open("logfile.txt", "w")

@dataclass
class Tile:
    state: str
    closedCount: int
    flaggedCount: int
    closedGroup: list = field(default_factory=list)

# MEDIUM BOARD - 16x16
BOARD_TOP = 493
BOARD_LEFT = 878
BOARD_WIDTH = 576
BOARD_HEIGHT = 576
EMOJI_TOP = 405
EMOJI_LEFT = 1139
EMOJI_WIDTH = 55
EMOJI_HEIGHT = 55

ROWS, COLS = 16, 16
CELL_SIZE = BOARD_WIDTH // ROWS # 36
BOARD = [[Tile(state="-", closedCount=0, flaggedCount=0, closedGroup=[]) for i in range(COLS)] for j in range(ROWS)]

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

def getClosedNeighbours(row, col):
    closedNeighbours = []
    neighbours = getNeighbours(row, col)

    for i, j in neighbours:
        if BOARD[i][j].state == "-":
            closedNeighbours.append((i,j))
    
    return closedNeighbours

def checkBombPairs(neighbours):
    temp = []
    for i, j in neighbours:

        if BOARD[i][j].state in ["-", "0", "*"]:
            continue

        if int(BOARD[i][j].state) - BOARD[i][j].flaggedCount == 1:
            temp.append((i,j))
    
    return temp

# get the closedCount, flaggedCount, closedGroup attributes
def getTileCounts(row, col, neighbours):
    closedCount = 0
    flaggedCount = 0
    closedGroup = []

    for i, j in neighbours:
        if BOARD[i][j].state == "-":
            closedCount += 1
            closedGroup.append((i,j))
        elif BOARD[i][j].state == "*":
            flaggedCount += 1
    
    BOARD[row][col].closedCount = closedCount
    BOARD[row][col].flaggedCount = flaggedCount
    BOARD[row][col].closedGroup = closedGroup

# =========== Action Functions ===========

def openClosedNeighbours(neighbours):
    for i, j in neighbours:
        if BOARD[i][j].state == "-":
            BOARD[i][j].state = "-1"
            mouse.leftClickCell(i, j)

def openTile(row, col):
    if BOARD[row][col].state == "-":
        BOARD[row][col].state = "-1"
        mouse.leftClickCell(row, col)

def flagClosedNeighbours(neighbours):
    for i, j in neighbours:
        if BOARD[i][j].state == "-":
            BOARD[i][j].state = "*"
            mouse.rightClickCell(i, j)

def flagTile(row, col):
    if BOARD[row][col].state == "-":
        BOARD[row][col].state = "*"
        mouse.rightClickCell(row, col)
    
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

            # number of closed, flagged neighbours updated
            getTileCounts(row, col, neighbours)

            if int(tile.state) == tile.closedCount + tile.flaggedCount:
                flagClosedNeighbours(neighbours)
            
            if int(tile.state) == tile.flaggedCount:
                openClosedNeighbours(neighbours)
            
            # check if any neighbour has reduced bomb count of 1
            # if so, check their closedGroup
            # if int(closedNeigbours - closedGroup) = int(state), flag all

            closedNeighbours = tile.closedGroup
            possibleNeighbours = checkBombPairs(neighbours)

            for i, j in possibleNeighbours:
                possibleGroup = getClosedNeighbours(i, j)
                
                if len(possibleGroup) <= 1:
                    continue

                # check if all possibleGroup is in closedNeighbours
                if set(possibleGroup).issubset(set(closedNeighbours)):
                    result = list(set(closedNeighbours) - set(possibleGroup))

                    if len(result) == 0:
                        continue
                    
                    text = "Coord: (" + str(row) + "," + str(col) + ")\nResults: " + str(result)
                    log.write(text)
                    text = "\nClosed: " + str(tile.closedCount) + " Flagged: " + str(tile.flaggedCount)
                    log.write(text)
                    text = "\nMain Cell Closed Neighbours: " + str(closedNeighbours)
                    log.write(text)
                    text = "\nNeighbours Containing Max One Mine: " + str(possibleGroup) + "\n\n"
                    log.write(text)

                    if int(tile.state) == 1 and tile.flaggedCount == 0:
                        for resRow, resCol in result:
                            openTile(resRow, resCol)
                    
                    if int(tile.state) == 2 and tile.flaggedCount == 1:
                        for resRow, resCol in result:
                            openTile(resRow, resCol)
                    
                    if int(tile.state) - tile.flaggedCount == len(result) + 1:
                        for resRow, resCol in result:
                            flagTile(resRow, resCol)

# take screenshot of the board
with mss.mss() as sct:
    # The screen part to capture
    monitor = {"top": BOARD_TOP, "left": BOARD_LEFT, "width": BOARD_WIDTH, "height": BOARD_HEIGHT}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    monitor2 = {"top": EMOJI_TOP, "left": EMOJI_LEFT, "width": EMOJI_WIDTH, "height": EMOJI_HEIGHT}
    output2 = "sct-{top}x{left}_{width}x{height}.png".format(**monitor2)
    
    while True:
        # Grab the data
        ss_board = sct.grab(monitor)
        ss_emoji = sct.grab(monitor2)
        ssToArr(ss_board)

        if ss_emoji.pixel(33, 20) == (0,0,0):
            break

        processBoard()

    # Save to the picture file
    mss.tools.to_png(ss_board.rgb, ss_board.size, output=output)
    mss.tools.to_png(ss_emoji.rgb, ss_emoji.size, output=output2)

log.close()