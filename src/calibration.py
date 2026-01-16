import mss
import config

def configureBoard(rgb1, rgb2):
    # take screenshot, save it into variable
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        ss = sct.grab(monitor)
        mss.tools.to_png(ss.rgb, ss.size, output="screen.png")

    # extract image values
    width = ss.size.width
    height = ss.size.height
    pixels = ss.pixels

    coords1 = None
    coords2 = None

    # find top-left corner, first pixel that matches the color
    found = False
    for i in range(width):
        for j in range(height):
            if pixels[j][i] == rgb1:
                coords1 = (i, j)
                found = True
                break
        if found:
            break
    
    # find bottom-right corner, last pixel that matches the color
    found = False
    for i in reversed(range(width)):
        for j in reversed(range(height)):
            if pixels[j][i] == rgb2:
                coords2 = (i, j)
                found = True
                break
        if found:
            break

    if coords1 is None:
        raise ValueError("Couldn't find top-left corner pixel")
    if coords2 is None:
        raise ValueError("Couldn't find bottom-right corner pixel")
    print(coords1, coords2)
    left, top = coords1
    right, bottom = coords2
    width = right - left + 1
    height = bottom - top + 1

    # screenshot of board
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        output = config.DATA_DIR + "/configuration.png".format(**monitor)

        ss_board = sct.grab(monitor)

        mss.tools.to_png(ss_board.rgb, ss_board.size, output=output)
    
    # calculate config variables
    cellsInRow = computeEdgeCount(ss_board)
    cellSize = width // cellsInRow
    cellsInColumn = height // cellSize

    emojiOffsetX = round(cellSize * 0.167)
    emojiOffsetY = round(cellSize * 1.889)

    emojiX = left + (cellsInRow // 2) * cellSize + emojiOffsetX
    emojiY = top - emojiOffsetY

    # set config variables
    config.BOARD_TOP = top
    config.BOARD_LEFT = left
    config.BOARD_WIDTH = width
    config.BOARD_HEIGHT = height
    config.ROWS = cellsInRow
    config.COLS = cellsInColumn
    config.CELL_SIZE = cellSize
    config.EMOJI_CHECK_COORDS = (emojiX, emojiY)

# a = (r1, g1, b1), b = (r2, g2, b2)
# zip(a, b) = [(r1, r2), (g1, g2), (b1, b2)]
def colorDifference(a, b, tolerance=8):
    return any(abs(x - y) > tolerance for x, y in zip(a, b))

def computeEdgeCount(ss):
    firstRow = ss.pixels[0]
    differences = 0

    for i in range(1, len(firstRow)):
        if colorDifference(firstRow[i], firstRow[i-1]):
            differences += 1

    return (differences+1)//2