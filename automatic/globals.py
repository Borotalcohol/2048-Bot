def init():
    global DIRECTIONS_MAP, WIDTH, HEIGHT, SQUARE_SIZE, BG_COLOR, MAIN_SQUARE_COLOR, EMPTY_SQUARE_COLOR, DARK_TEXT_COLOR, LIGHT_TEXT_COLOR, TILE_COLORS

    WIDTH = 500
    HEIGHT = 500

    SQUARE_SIZE = WIDTH - 40

    BG_COLOR = "#FAF8EF"
    MAIN_SQUARE_COLOR = "#BBADA0"
    EMPTY_SQUARE_COLOR = "#CDC0B4"

    DARK_TEXT_COLOR = "#776E65"
    LIGHT_TEXT_COLOR = "#F9F6F2"

    TILE_COLORS = {
        2: "#EEE4DA",
        4: "#EDE0C8",
        8: "#F2B179",
        16: "#F59563",
        32: "#F67C5F",
        64: "#F65E3B",
        128: "#EDCF72",
        256: "#EDCC61",
        512: "#EDC850",
        1024: "#EDC53F",
        2048: "#EDC22E",
        4096: "#5EDA92",
        8192: "#27BB67",
        16384: "#74B5DD",
        32768: "#5EA1E1",
        65536: "#007FC2"
    }

    DIRECTIONS_MAP = {
        0: "up",
        1: "down",
        2: "left",
        3: "right",
    }