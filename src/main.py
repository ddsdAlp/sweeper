import mss
from dataclasses import dataclass, field
import mouse
import calibration
import config

@dataclass
class Tile:
    state: str
    closedCount: int
    flaggedCount: int
    closedGroup: list = field(default_factory=list)

# print the BOARD array
def printBoard():
    for row in range(config.ROWS):
        temp = ""
        for col in range(config.COLS):
            temp = temp + str(BOARD[row][col].state) + " "
        print(temp)

# turn screenshot into BOARD array
def screenshotToArray(img):
    for row in range(config.ROWS):
        rowCoord = row * config.CELL_SIZE
        for col in range(config.COLS):
            colCoord = col * config.CELL_SIZE
            topLeftRGB = img.pixel(colCoord, rowCoord)
            typeCheckRGB = img.pixel(colCoord + round(0.6 * config.CELL_SIZE), rowCoord + round(0.73 * config.CELL_SIZE))

            # closed
            if topLeftRGB == (112, 120, 128):
                if img.pixel(colCoord + config.CELL_SIZE//2 - 1, rowCoord + config.CELL_SIZE//2 - 1) == (102, 221, 102):
                    BOARD[row][col].state = "x"
                elif typeCheckRGB in config.COLOR_DICT:
                    BOARD[row][col].state = config.COLOR_DICT[typeCheckRGB]
                else:
                    BOARD[row][col].state = "-"
            # opened
            elif topLeftRGB == (30, 38, 46):
                if typeCheckRGB in config.COLOR_DICT:
                    BOARD[row][col].state = config.COLOR_DICT[typeCheckRGB]
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

def getFlaggedNeighbours(row, col):
    flaggedNeighbours = []
    neighbours = getNeighbours(row, col)

    for i, j in neighbours:
        if BOARD[i][j].state == "*":
            flaggedNeighbours.append((i,j))
    
    return flaggedNeighbours

def checkBombPairs(neighbours):
    temp = []
    for i, j in neighbours:
        if BOARD[i][j].state in ["-", "0", "*"]:
            continue
        
        flagged = getFlaggedNeighbours(i, j)

        if int(BOARD[i][j].state) - len(flagged) == 1:
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
    if BOARD[row][col].state in ["-", "x"]:
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
    for row in range(config.ROWS):
        for col in range(config.COLS):
            tile = BOARD[row][col]

            # skip unnecessarry tiles
            if tile.state in ["-", "0", "*"]:
                continue

            if tile.state == "x":
                openTile(row, col)
                continue
            
            # get all neighbour coords
            neighbours = getNeighbours(row, col)

            # number of closed, flagged neighbours updated
            getTileCounts(row, col, neighbours)

            # ===== basic pattern 1 =====
            if int(tile.state) == tile.closedCount + tile.flaggedCount:
                flagClosedNeighbours(neighbours)
            
            # ===== basic pattern 2 =====
            if int(tile.state) == tile.flaggedCount:
                openClosedNeighbours(neighbours)

            # ===== complex pattern =====
            closedNeighbours = tile.closedGroup
            possibleNeighbours = checkBombPairs(neighbours)

            for i, j in possibleNeighbours:
                possibleGroup = getClosedNeighbours(i, j)
                if len(possibleGroup) <= 1:
                    continue
                
                result = list(set(closedNeighbours) - set(possibleGroup))
                if len(result) == 0:
                    continue
                
                # check the scenarios if all possibleGroup is in closedNeighbours
                if set(possibleGroup).issubset(set(closedNeighbours)):
                    
                    text = "Coord: (" + str(row) + "," + str(col) + ")\nResults: " + str(result)
                    log.write(text)
                    text = "\nClosed: " + str(tile.closedCount) + " Flagged: " + str(tile.flaggedCount)
                    log.write(text)
                    text = "\nMain Cell Closed Neighbours: " + str(closedNeighbours)
                    log.write(text)
                    text = "\nNeighbours Containing Max One Mine: " + str(possibleGroup) + "\n\n"
                    log.write(text)
                    
                    # if bomb link in neighbours and there are no other bombs
                    if int(tile.state) - tile.flaggedCount == 1:
                        for resRow, resCol in result:
                            openTile(resRow, resCol)
                    
                    # if bomb link in neighbours and there are no other possible closed tiles
                    if int(tile.state) - tile.flaggedCount == len(result) + 1:
                        for resRow, resCol in result:
                            flagTile(resRow, resCol)

                # check the scenarios if not
                else:
                    # ! might not work !
                    # length of possible group already checked before, possibleGroup is >= 2
                    # if bomb link not completely in neighbours but no other possible closed tiles
                    if int(tile.state) - tile.flaggedCount - 1 == len(result):
                        for resRow, resCol in result:
                            flagTile(resRow, resCol)                   

print("\nStarting solver...")
log = open(config.LOG_FILE_PATH, "w")

entireBoardRGB1 = (120, 128, 136)
entireBoardRGB2 = (30, 38, 46)

mineBoardRGB1 = (112, 120, 128)
mineBoardRGB2 = (34, 42, 50)

# Find the minesweeper board and configure the values in config.py
# calibration.configureBoard(mineBoardRGB1, mineBoardRGB2)

# create our own board
BOARD = [[Tile(state="-", closedCount=0, flaggedCount=0, closedGroup=[]) for i in range(config.COLS)] for j in range(config.ROWS)]

# take screenshot of the board
with mss.mss() as sct:
    # The screen part to capture
    monitor = {"top": config.BOARD_TOP, "left": config.BOARD_LEFT, "width": config.BOARD_WIDTH, "height": config.BOARD_HEIGHT}
    output = config.DATA_DIR + "/board-{top}x{left}_{width}x{height}.png".format(**monitor)

    # monitor2 = {"top": config.EMOJI_TOP, "left": config.EMOJI_LEFT, "width": config.EMOJI_WIDTH, "height": config.EMOJI_HEIGHT}
    # output2 = config.DATA_DIR + "/emoji-{top}x{left}_{width}x{height}.png".format(**monitor2)
    
    monitor3 = sct.monitors[1]
    
    emojiX, emojiY = config.EMOJI_CHECK_COORDS

    # main solver loop
    while True:

        # grab the board and emoji data
        ss_board = sct.grab(monitor)
        # ss_emoji = sct.grab(monitor2)
        ss_screen = sct.grab(monitor3)

        # save to the picture file
        mss.tools.to_png(ss_board.rgb, ss_board.size, output=output)
        # mss.tools.to_png(ss_emoji.rgb, ss_emoji.size, output=output2)
        # mss.tools.to_png(ss_screen.rgb, ss_screen.size, output="screen.png")

        screenshotToArray(ss_board)
        
        emojiCheck = ss_screen.pixel(emojiX, emojiY)
        # break condition, win or fail
        if not calibration.colorDifference(emojiCheck, (0,0,0), tolerance=5):
            print("Stop condition reached.")
            break
        
        # solver logic
        processBoard()

log.close()