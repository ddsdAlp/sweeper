from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE_PATH = str(BASE_DIR / "data" / "logfile.txt")

# MEDIUM BOARD - 16x16
BOARD_TOP = 493
BOARD_LEFT = 878
BOARD_WIDTH = 576
BOARD_HEIGHT = 576
EMOJI_TOP = 405
EMOJI_LEFT = 1139
EMOJI_WIDTH = 55
EMOJI_HEIGHT = 55

ROWS = 16
COLS = 16
CELL_SIZE = BOARD_WIDTH // ROWS # 36

COLOR_DICT = {
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