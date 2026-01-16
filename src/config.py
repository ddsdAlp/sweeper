from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parent.parent)
DATA_DIR = BASE_DIR + "/data"
LOG_FILE_PATH = DATA_DIR + "/logfile.txt"

# MEDIUM BOARD, Opera   Chrome
BOARD_TOP =     493     # 383
BOARD_LEFT =    878     # 598
BOARD_WIDTH =   576     # 480
BOARD_HEIGHT =  576     # 480
EMOJI_TOP = 405
EMOJI_LEFT = 1139
EMOJI_WIDTH = 55
EMOJI_HEIGHT = 55
EMOJI_CHECK_COORDS = (0,0)  #(1172, 425)

ROWS = 16
COLS = 16
CELL_SIZE = BOARD_WIDTH // ROWS

COLOR_DICT = {
    (102, 221, 102) : "start", # X
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