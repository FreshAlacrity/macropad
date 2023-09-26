# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

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
from tamtam import all_faces
from tamtam import tam_tam_faces
from mappings import current_layer_name



DISPLAY_SETTINGS = {
    "FONT_CHOICE": 0,
    "FONT_DIR": "fonts/",
    "FONT_FILE": "ucs-fonts/6x9.bdf"
}

def init():
    DISPLAY_SETTINGS["FONT"] = bitmap_font.load_font(f"{DISPLAY_SETTINGS['FONT_DIR']}{DISPLAY_SETTINGS['FONT_FILE']}")
    DISPLAY_SETTINGS["CHAR_WIDTH"] = int(DISPLAY_SETTINGS["FONT_FILE"][10])
    char_height = int(DISPLAY_SETTINGS["FONT_FILE"][12])
    if DISPLAY_SETTINGS["FONT_FILE"][13] != ".":
        char_height = int(DISPLAY_SETTINGS["FONT_FILE"][slice(12, 13)])
    DISPLAY_SETTINGS["CHAR_HEIGHT"] = char_height
    
    # Assign default palette colors
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF
    DISPLAY_SETTINGS["PALETTE"] = palette
    
    # DISPLAY IO SETUP
    # Create a bitmap (sprite sheet) with two colors
    DISPLAY_SETTINGS["MAIN_BITMAP"] = create_main_bitmap()
    
    # Create a TileGrid using the Bitmap and Palette
    DISPLAY_SETTINGS["TILE_GRID"] = displayio.TileGrid(DISPLAY_SETTINGS["MAIN_BITMAP"], pixel_shader=DISPLAY_SETTINGS["PALETTE"])

    # Create a Group and add the main TileGrid
    DISPLAY_SETTINGS["MAIN_GROUP"] = displayio.Group()
    DISPLAY_SETTINGS["MAIN_GROUP"].append(DISPLAY_SETTINGS["TILE_GRID"])


START_TIME = time.monotonic()
OLED_DISPLAY = board.DISPLAY
OLED_DISPLAY.auto_refresh = False

def create_main_bitmap():
    return displayio.Bitmap(OLED_DISPLAY.width, OLED_DISPLAY.height, 2)

def create_sprite_sheet():
    # @todo get faces printed to this
    char_width = DISPLAY_SETTINGS["CHAR_WIDTH"]
    char_height = DISPLAY_SETTINGS["CHAR_HEIGHT"]
    tile_width = char_width * 5
    
    # Create a bitmap (sprite sheet) with two colors
    bitmap = displayio.Bitmap(tile_width, char_height * 2, 2)
    
    # Assign colors to the bitmap
    palette = DISPLAY_SETTINGS["PALETTE"]
    
    tile_grid = displayio.TileGrid(bitmap, 
                                   tile_width=tile_width, 
                                   tile_height=char_height,
                                   pixel_shader=palette)
    
    return displayio.Bitmap(OLED_DISPLAY.width, OLED_DISPLAY.height, 2)





def display_bitmap_text(string, sx=0, sy=0):  # , frame):
    # see https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font/blob/main/examples/bitmap_font_label_simpletest.py
    # @later detect unsupported characters
    font = DISPLAY_SETTINGS["FONT"]
    char_height = DISPLAY_SETTINGS["CHAR_HEIGHT"]
    
    # Create the text label
    text_area = label.Label(font, text=string, color=0xFFFFFF)

    # Set the location
    text_area.x = sx
    text_area.y = sy + char_height // 2

    # Show it
    return(text_area)


def centered_text(string, sy=10):
    char_width = DISPLAY_SETTINGS["CHAR_WIDTH"]
    width = len(string) * char_width
    sx = (OLED_DISPLAY.width - width) // 2
    return display_bitmap_text(string, sx, sy)


def multi_line_text(string, sx, sy):
    # @todo do automatic linebreaks/scroll animation according to character width
    lines = [string]
    char_width = DISPLAY_SETTINGS["CHAR_WIDTH"]
    one_line = OLED_DISPLAY.width // char_width
    print(f"Bitmap Output:\n{string}")
    if len(string) > one_line:
        for index, char in enumerate(string):
            if char == " " or index == one_line:
                lines = [string[slice(0, index)], string[slice(index)]]
    
    # @todo figure out how to return multiple line objects combined
    return display_bitmap_text("\n".join(lines), sx, sy)
    

def draw_pixel(bitmap, x=20, y=30, index=1):
    # Draw a pixel - X is 0-63, Y is 0-127
    bitmap[x, y] = index


def draw_rect(sx, sy, w, h):
    if sx + w > 63 or sy + h > 127:
        raise Exception(f"Trying to draw outside the range! {sx},{sy},{w},{h}")

    for x in range(sx, sx + w):
        for y in range(sy, sy + h):
            DISPLAY_SETTINGS["MAIN_BITMAP"][x, y] = 1


def update_display():
    # progress()
    # draw_pixel()

    DISPLAY_SETTINGS["MAIN_GROUP"].append(tam_tam())
    DISPLAY_SETTINGS["MAIN_GROUP"].append(multi_line_text(current_layer_name(), 0, 100))
    
    # Add the Group to the Display
    OLED_DISPLAY.show(DISPLAY_SETTINGS["MAIN_GROUP"])
    
    # Updates the display
    OLED_DISPLAY.refresh()
    
    # Never shows up on the display,
    # regardless of if it's before or after refresh:
    # print("HELLO WORLD")


def progress_bar():
    """Adds a tamtam face to the current display group"""
    frames = OLED_DISPLAY.width
    # @todo put a bar at the end so it's clear what full progress looks like
    frames_elapsed = int(
        (time.monotonic() - START_TIME) * 5 / (frames - 1)
    )
    frame = frames_elapsed % frames
    print(f"Frame {frame} of {frames}")
    draw_rect(0, 50, frame, 10)


def tam_tam(mood="egg"):
    """Adds a tamtam face to the current display group"""
    frames = 2
    # tam_tam_faces()[face]["faces"]
    # mood_data = TAM_TAM_FACES
    frames_elapsed = int(
        (time.monotonic() - START_TIME) * 5 / (frames - 1)
    )
    frame = 1  # frames_elapsed % frames
    current_face = all_faces()[frame]  # @todo update
    # current_face = mood_data["faces"][frame]
    # print(f"Frame {frames_elapsed} -> {frame}")
    return centered_text(current_face)


init()