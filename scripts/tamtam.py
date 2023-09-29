# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member, no-name-in-module


# pylint: disable=no-value-for-parameter, broad-exception-raised

from board import DISPLAY
from displayio import Bitmap as new_bitmap
from displayio import Palette as new_palette
from displayio import Group as new_group
from displayio import TileGrid as new_tile_grid
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font
from adafruit_bitmapsaver import save_pixels
from timetest import time_test
from logger import log


SETTINGS = {
    "FONT_PATH": "fonts/ucs-fonts/7x13.bdf",
    "OLED_DISPLAY": DISPLAY,
}

SPRITES = {"PALETTE": new_palette(2)}


def all_faces():
    return [
        "  o  ",
        "  O  ",
        "∩ _ ∩",  # 2
        "O ◡ O",
        "- ◡ -",
        "• _ •",
        "- _ -",
        "> _ >",
        "< _ <",  # 8
        "> _ <",
        "X _ X",  # 10
        "° _ °",
        "- o -",
        "- w -",
        "- θ -",  # 14
        "¬ ◡ ¬",
        "¬ _ ¬",
        "υ _ υ",  # 17
        "џ _ џ",
        "ὺ _ ύ",
        "ὸ _ ό",
        "O Д O",
        "; Д ;",
        "T _ T",  # 23
        "τ _ τ",
        "v _ v",
        "n _ n",
        "O ω O",
        "ὲ ◡ έ",
        "ὶ ◡ ί",
        "Ξ ◡ Ξ",
        "' o '",
        "∩ _ ∩",
        "- ◡ O",  # 34 - THIS IS WHERE MEMORY ALLOCATION FAILS
        "c(_) ",
        # "⚆ _ ⚆",  # Unsupported glyph
        "# _ #",
    ]


def tam_tam_faces(mood):
    faces = {
        "all": {
            "faces": range(len(all_faces())),
            "frames": 4,
        },
        "egg": {"faces": [0, 1], "frames": 10},
        "happy": {
            "faces": [3, 4],
            "frames": 4,
        },
        "neutral": {
            "faces": [5, 7, 5, 8, 5, 6],
            "frames": 6,
        },
        "tea": {
            "faces": [2, 34],
            "frames": 6,
        },
        "eating": {
            "faces": [2, 12, 14],
            "frames": 6,
        },
        "sick": {
            "faces": [10, 9],
            "frames": 6,
        },
        "asleep": {
            "faces": [6, 6, 12],
            "frames": 21,
        },
        "sad": {
            "faces": [17, 18, 19],
            "frames": 6,
        },
        "scared": {
            "faces": [11, 21, 22],
            "frames": 4,
        },
        "angry": {
            "faces": [16, 20, 9],
            "frames": 4,
        },
        "hungry": {
            "faces": [24, 9],
            "frames": 4,
        },
        "bored": {
            "faces": [17, 5, 6, 16],
            "frames": 3,
        },
        "tired": {
            "faces": [25, 17],
            "frames": 3,
        },
        "sneaky": {
            "faces": [15, 27, 28, 29, 26],
            "frames": 4,
        },
        "random": {
            "faces": [30, 31, 32, 33, 26],
            "frames": 1,
        },
    }
    return faces[mood]["faces"]


def current_face_string(elapsed_time):
    """Returns a string value containing the current tamtam face expression"""
    mood = "all"
    indexes = tam_tam_faces(mood)
    frames_elapsed = int(elapsed_time * 30 / (len(indexes) - 1))
    frame = frames_elapsed % len(indexes)
    current_face = all_faces()[indexes[frame]]
    if len(current_face) != SETTINGS["TAM_TAM_WIDTH"]:
        log("Frame", frame)
        log("Indexes", indexes[frame])
        raise Exception(f"Oops! '{current_face}' is not the right length")
    return current_face


def unique_chars():
    # Get all characters in all faces (including spaces)
    string = "".join(all_faces())

    # Split and deduplicate the list of characters
    chars = list(dict.fromkeys(list(string)))
    return chars


def font_setup():
    """Gets the font details and loads the font"""
    SETTINGS["FONT"] = bitmap_font.load_font(SETTINGS["FONT_PATH"])

    font_dimensions = SETTINGS["FONT_PATH"].split("/")
    while len(font_dimensions) > 2:
        del font_dimensions[0]
    font_dimensions = font_dimensions[len(font_dimensions) - 1]
    font_dimensions = font_dimensions.split("x")
    SETTINGS["CHAR_WIDTH"] = int(font_dimensions[0])
    font_dimensions = font_dimensions[1].split(".")
    SETTINGS["CHAR_HEIGHT"] = int(font_dimensions[0])

    SETTINGS["Y_HEIGHT"] = SETTINGS["CHAR_HEIGHT"] // 2


@time_test("Set up tile grid")
def set_up_tile_grid(canvas):
    SPRITES["PALETTE"][0] = 0x000000
    SPRITES["PALETTE"][1] = 0xFFFFFF
    return new_tile_grid(
        canvas,
        pixel_shader=SPRITES["PALETTE"],
        width=SETTINGS["TAM_TAM_WIDTH"],
        height=1,
        tile_width=SETTINGS["CHAR_WIDTH"],
        tile_height=SETTINGS["CHAR_HEIGHT"],
    )


@time_test("Make sprite sheet")
def make_sprite_sheet():
    """Creates a displayio TileGrid containing all the different parts of the tamtam faces to be used as sprites"""
    
    @time_test("Make char")
    def make_sprite(char):
        return bitmap_label.Label(SETTINGS["FONT"], text=char, color=0xFFFFFF)

    # @todo figure out why there's a few lines of pixels + a red one at the top of the bitmap
    # @later try also saving the 1/0 bitmaps to more condensed formats?

    # List all the characters to make into sprites
    SPRITES["LIST"] = unique_chars()

    # Make a canvas for our sprites
    width = SETTINGS["CHAR_WIDTH"] * len(SPRITES["LIST"])
    height = SETTINGS["CHAR_HEIGHT"]
    canvas = new_bitmap(width, height, 2)

    # Add each character to the canvas
    for c in SPRITES["LIST"]:
        # @todo
        # SPRITES[c] = make_sprite(c)
        pass

    for x in range(width // 2):
        for y in range(height // 2):
            # @todo could load in the character data here directly?
            canvas[x * 2, y * 2] = 1

    # Make a tile grid for tamtam faces that we can display canvas tiles to
    SPRITES["TILE_GRID"] = set_up_tile_grid(canvas)

    # Attempt to save the spritesheet in case the drive is writable
    try:
        save_pixels("sprite_sheet.bmp", canvas, SPRITES["PALETTE"])
        log("Bitmap saved!")
    except OSError as _:
        # Typical error when the filesystem isn't writeable
        log("Sprite sheet not exported because the drive is in USB mode")


@time_test("Make string bitmap")
def update_tile_grid(string, sx=0, sy=0):
    # see https://learn.adafruit.com/circuitpython-display-support-using-displayio/tilegrid-and-group
    # @todo update this later when there's more than one row:
    def get_sprite_position(char):
        return SPRITES["LIST"].index(char)

    # Add each sprite in the new face
    for index, char in enumerate(string):
        SPRITES["TILE_GRID"][index] = get_sprite_position(char)

    # For now just return an empty group  @todo
    group = new_group()
    return group


def centered_text(string, sy=10):
    width = len(string) * SETTINGS["CHAR_WIDTH"]
    sx = (SETTINGS["OLED_DISPLAY"].width - width) // 2
    bitmap = update_tile_grid(string, sx, sy)
    return bitmap


def current_face_sprite(face_string, sy):
    # @todo test the time this takes against a spritesheet
    return centered_text(face_string, sy)


def get_expression_width():
    """Checks through all the tam tam expressions and returns the length of the longest string"""
    return max(map(len, all_faces()))

def init():
    font_setup()
    SETTINGS["TAM_TAM_WIDTH"] = get_expression_width()
    make_sprite_sheet()


init()
