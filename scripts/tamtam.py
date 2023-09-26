# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, pointless-string-statement, missing-function-docstring

import time
import board
import displayio

"""
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle
"""
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from faces import tam_tam_faces

TAM_TAM_FACES = tam_tam_faces()
FONT_CHOICE = 0
FONT_DIR = "fonts/"
FONT_FILE = "ucs-fonts/6x9.bdf"
CHAR_WIDTH = int(FONT_FILE[10])
CHAR_HEIGHT = int(FONT_FILE[12])  # @todo get 2 digit heights working?
if FONT_FILE[13] != ".":
    CHAR_HEIGHT = int(FONT_FILE[slice(12, 13)])
print(f"Width: {CHAR_WIDTH}  Height: {CHAR_HEIGHT}")
FONT = bitmap_font.load_font(f"{FONT_DIR}{FONT_FILE}")
START_TIME = time.monotonic()
OLED_DISPLAY = board.DISPLAY
OLED_DISPLAY.auto_refresh = False

# DISPLAY IO SETUP
# Create a bitmap with two colors
bitmap = displayio.Bitmap(OLED_DISPLAY.width, OLED_DISPLAY.height, 2)

# Create a two color palette
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xFFFFFF

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)
    
def display_bitmap_text(string, s_x=0, s_y=0):
    # see https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font/blob/main/examples/bitmap_font_label_simpletest.py

    # use built in display (MagTag, PyPortal, PyGamer, PyBadge, CLUE, etc.)
    # see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
    # https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus

    # @todo detect unsupported characters
    # @todo do automatic linebreaks according to character width

    print(f"Bitmap Output:\n{string}")

    # Create the text label
    text_area = label.Label(FONT, text=string, color=0xFFFFFF)

    # Set the location
    text_area.x = s_x
    text_area.y = s_y + CHAR_HEIGHT // 2

    # Show it
    OLED_DISPLAY.show(text_area)  # pylint: disable=no-member


def centered_text(string, s_y=10):
    width = len(string) * CHAR_WIDTH
    s_x = (OLED_DISPLAY.width - width) // 2
    display_bitmap_text(string, s_x, s_y)


def draw_pixel():
    # Draw a pixel - X is 0-63, Y is 0-127
    bitmap[20, 30] = 1


def draw_rect(sx, sy, w, h):
    if sx + w > 63 or sy + h > 127:
        raise Exception(f"Trying to draw outside the range! {sx},{sy},{w},{h}")

    for x in range(sx, sx + w):
        for y in range(sy, sy + h):
            bitmap[x, y] = 1


def update_display():
    draw_rect(0, 50, 50, 10)
    # draw_pixel()

    # Add the Group to the Display
    # OLED_DISPLAY.show(group)
    
    # @TODO figure out why this overwrites the displayio things
    tam_tam()  # Needs to be followed by refresh
    OLED_DISPLAY.refresh()

    # Never shows on the display,
    # regardless of if it's before or after refresh:
    # print("HELLO WORLD")


def tam_tam(face="neutral"):
    mood_data = TAM_TAM_FACES[face]
    frames_elapsed = int(
        (time.monotonic() - START_TIME) * 5 / (mood_data["frames"] - 1)
    )
    frame = frames_elapsed % len(mood_data["faces"])
    current_face = mood_data["faces"][frame]
    print(f"Frame {frames_elapsed} -> {frame}")
    centered_text(current_face)
    # why isn't this putting the |||| on the last row? nothing shows there?!
