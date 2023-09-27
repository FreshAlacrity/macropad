# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, pointless-string-statement, missing-function-docstring

import time
import board
import displayio
from adafruit_display_shapes.rect import Rect
# from adafruit_display_shapes.circle import Circle
# from adafruit_display_shapes.triangle import Triangle
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from tamtam import all_faces
from tamtam import tam_tam_faces
from mappings import current_layer_name


DISPLAY_SETTINGS = {
    "FONT_CHOICE": 0,
    "FONT_DIR": "fonts/",
    "FONT_FILE": "ucs-fonts/7x13.bdf",
    "START_TIME": time.monotonic(),
    "OLED_DISPLAY": board.DISPLAY,
    "PROGRESS_BAR_HEIGHT": 40
}
STORAGE = {
    "layer_names": {}
}

def init():
    # Display setup
    DISPLAY_SETTINGS["OLED_DISPLAY"].auto_refresh = False
    
    # Font loading and setup
    DISPLAY_SETTINGS["FONT"] = bitmap_font.load_font(f"{DISPLAY_SETTINGS['FONT_DIR']}{DISPLAY_SETTINGS['FONT_FILE']}")
    
    font_dimensions = DISPLAY_SETTINGS["FONT_FILE"].split("/")
    font_dimensions = font_dimensions[len(font_dimensions) - 1]
    font_dimensions = font_dimensions.split("x")
    DISPLAY_SETTINGS["CHAR_WIDTH"] = int(font_dimensions[0])
    font_dimensions = font_dimensions[1].split(".")
    DISPLAY_SETTINGS["CHAR_HEIGHT"] = int(font_dimensions[0])
    print(DISPLAY_SETTINGS["CHAR_WIDTH"], DISPLAY_SETTINGS["CHAR_HEIGHT"])
    
    # Assign default palette colors
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF
    DISPLAY_SETTINGS["PALETTE"] = palette


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
    
    # Draws a single white pixel:
    # bitmap[x, y] = 1
    
    return displayio.Bitmap(DISPLAY_SETTINGS["OLED_DISPLAY"].width, DISPLAY_SETTINGS["OLED_DISPLAY"].height, 2)

def make_string_bitmap(string):
    if False: # string in STORAGE["layer_names"]:
        return STORAGE["layer_names"][string]
    else:
        font = DISPLAY_SETTINGS["FONT"]
        
        # Create the text label
        text_area = label.Label(font, text=string, color=0xFFFFFF)
        STORAGE["layer_names"][string] = text_area
        return text_area
        
def display_bitmap_text(string, sx=0, sy=0):  # , frame):
    char_height = DISPLAY_SETTINGS["CHAR_HEIGHT"]
    text_area = make_string_bitmap(string)

    # Set the location
    text_area.x = sx
    text_area.y = sy + char_height // 2

    return(text_area)


def centered_text(string, sy=10):
    char_width = DISPLAY_SETTINGS["CHAR_WIDTH"]
    width = len(string) * char_width
    sx = (DISPLAY_SETTINGS["OLED_DISPLAY"].width - width) // 2
    return display_bitmap_text(string, sx, sy)


def multi_line_text(string, sx, sy):
    # @todo do automatic linebreaks/scroll animation according to character width
    lines = [string]
    char_width = DISPLAY_SETTINGS["CHAR_WIDTH"]
    one_line = DISPLAY_SETTINGS["OLED_DISPLAY"].width // char_width
    # print(f"Bitmap Output: {string}")
    if len(string) > one_line:
        for index, char in enumerate(string):
            if char == " " or index == one_line:
                lines = [string[slice(0, index)], string[slice(index)]]
    
    # @todo figure out how to return multiple line objects combined
    return display_bitmap_text("\n".join(lines), sx, sy)


def animation_frame(frames, delay):
    # Higher delay is faster
    fractional_seconds = time.monotonic() - DISPLAY_SETTINGS["START_TIME"]
    frames_elapsed = int(fractional_seconds * delay / (frames - 1))
    return frames_elapsed % frames


def progress_bar():
    """Adds a tamtam face to the current display group"""
    frames = DISPLAY_SETTINGS["OLED_DISPLAY"].width - 2
    y_height = DISPLAY_SETTINGS["PROGRESS_BAR_HEIGHT"]
    frame = animation_frame(frames=frames, delay=200)
    # Documentation here: https://docs.circuitpython.org/projects/display-shapes/en/latest/api.html#adafruit_display_shapes.rect.Rect
    return Rect(1, y_height, frame + 1, 10, fill=0xFFFFFF)


def tam_tam(mood="egg"):
    """Returns a bitmap tamtam face in the appropriate position"""
    # indexes = tam_tam_faces(mood)
    indexes = range(len(all_faces()))  # tam_tam_faces(mood)
    frame = animation_frame(frames=len(indexes), delay=30)
    # current_face = all_faces()[indexes[frame]]
    current_face = all_faces()[frame]
    return centered_text(current_face, 15)


def create_main_bitmap():
    return displayio.Bitmap(
            DISPLAY_SETTINGS["OLED_DISPLAY"].width,
            DISPLAY_SETTINGS["OLED_DISPLAY"].height,
            2
        )


def update_display():
    display_start_time = time.monotonic()
    
    # Create a bitmap (sprite sheet) with two colors
    DISPLAY_SETTINGS["MAIN_BITMAP"] = create_main_bitmap()
    
    # Create a TileGrid using the Bitmap and Palette
    DISPLAY_SETTINGS["TILE_GRID"] = displayio.TileGrid(
            DISPLAY_SETTINGS["MAIN_BITMAP"],
            pixel_shader=DISPLAY_SETTINGS["PALETTE"]
        )
    
    
    test_start_time = time.monotonic()
    
    # Create a Group and add the main TileGrid
    DISPLAY_SETTINGS["MAIN_GROUP"] = displayio.Group()
    DISPLAY_SETTINGS["MAIN_GROUP"].append(DISPLAY_SETTINGS["TILE_GRID"])
    
    DISPLAY_SETTINGS["MAIN_GROUP"].append(Rect(0, DISPLAY_SETTINGS["PROGRESS_BAR_HEIGHT"], DISPLAY_SETTINGS["OLED_DISPLAY"].width, 10, fill="None", outline=0xFFFFFF))
    DISPLAY_SETTINGS["MAIN_GROUP"].append(progress_bar())
    DISPLAY_SETTINGS["MAIN_GROUP"].append(tam_tam())

    
    vertical_offset = DISPLAY_SETTINGS["OLED_DISPLAY"].height - DISPLAY_SETTINGS["CHAR_HEIGHT"]
    DISPLAY_SETTINGS["MAIN_GROUP"].append(multi_line_text(current_layer_name(), 0, vertical_offset))
    
    # Add the Group to the Display
    DISPLAY_SETTINGS["OLED_DISPLAY"].show(DISPLAY_SETTINGS["MAIN_GROUP"])
    
    # Updates the display
    DISPLAY_SETTINGS["OLED_DISPLAY"].refresh()
    
    # Never shows up on the display,
    # regardless of if it's before or after refresh:
    # print("HELLO WORLD")
    print("Display test execution time:  ", time.monotonic() - test_start_time)
    print("Display update execution time:", time.monotonic() - display_start_time)

init()