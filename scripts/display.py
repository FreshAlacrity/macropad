# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, pointless-string-statement, missing-function-docstring, trailing-whitespace

import time
import board
import displayio
from adafruit_display_shapes.rect import Rect


# from adafruit_display_shapes.circle import Circle
# from adafruit_display_shapes.triangle import Triangle
from tamtam import current_face_string
from tamtam import current_face_sprite
from mappings import current_layer_name
from text import new_layer_bitmap


SETTINGS = {
    "START_TIME": time.monotonic(),
    "OLED_DISPLAY": board.DISPLAY,
    "PROGRESS_BAR_HEIGHT": 45,
    "brightness": 0.5,
}
STORAGE = {
    "GETTER": {"LAYER": current_layer_name},
    "MAKER": {"LAYER": new_layer_bitmap},
}


def init():
    # Display setup
    SETTINGS["OLED_DISPLAY"].auto_refresh = False
    SETTINGS["OLED_DISPLAY"].brightness = SETTINGS["brightness"]
    SETTINGS["OLED_DISPLAY"].root_group = displayio.Group()
    frame = SETTINGS["OLED_DISPLAY"].root_group

    # Assign default palette colors
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF
    SETTINGS["PALETTE"] = palette

    # Create a bitmap (sprite sheet) with two colors
    SETTINGS["MAIN_BITMAP"] = create_main_bitmap()
    
    # Set which local functions are used to
    # check values and construct objects
    STORAGE["GETTER"]["TAM_TAM"] = current_tam_tam_frame
    STORAGE["MAKER"]["TAM_TAM"] = tam_tam
    STORAGE["MAKER"]["BAR"] = progress_bar
    STORAGE["GETTER"]["BAR"] = current_progress
    
    # Create a TileGrid using the Bitmap and Palette
    SETTINGS["TILE_GRID"] = displayio.TileGrid(
        SETTINGS["MAIN_BITMAP"], pixel_shader=SETTINGS["PALETTE"]
    )

    # Add the main tile grid and tamtam frame
    frame.append(SETTINGS["TILE_GRID"])

    frame.append(
        Rect(
            0,
            SETTINGS["PROGRESS_BAR_HEIGHT"],
            SETTINGS["OLED_DISPLAY"].width,
            10,
            fill="None",
            outline=0xFFFFFF,
        )
    )


def elapsed_time():
    return time.monotonic() - SETTINGS["START_TIME"]


def current_tam_tam_frame():
    return current_face_string(elapsed_time())




def current_progress():
    delay = 200
    frames = SETTINGS["OLED_DISPLAY"].width - 2
    frames_elapsed = int(elapsed_time() * delay / (frames - 1))
    return (frames_elapsed % frames) + 1


def progress_bar(frame):
    """Adds a tamtam face to the current display group"""
    y_height = SETTINGS["PROGRESS_BAR_HEIGHT"]
    return Rect(1, y_height, frame, 10, fill=0xFFFFFF)


def tam_tam(current_face):
    """Returns a bitmap tamtam face in the appropriate position"""
    return current_face_sprite(current_face, 15)


def create_main_bitmap():
    return displayio.Bitmap(
        SETTINGS["OLED_DISPLAY"].width, SETTINGS["OLED_DISPLAY"].height, 2
    )


def get_group(value_type, value):
    # If there isn't storage of this type already, intilize that
    if not value_type in STORAGE:
        STORAGE[value_type] = {}

    if value in STORAGE[value_type]:
        # Retrieve and return the group holding this layer name
        return STORAGE[value_type][value]
    else:
        # Create a group for the new value and store it
        new_group = displayio.Group()
        new_group.append(STORAGE["MAKER"][value_type](value))
        STORAGE[value_type][value] = new_group
        return new_group



def check_and_update(value_type):
    current_value = STORAGE["GETTER"][value_type]()
    frame = SETTINGS["OLED_DISPLAY"].root_group

    stored = value_type in SETTINGS
    changed = not stored or SETTINGS[value_type] != current_value

    if stored and changed:
        frame.remove(get_group(value_type, SETTINGS[value_type]))
    if not stored or changed:
        frame.append(get_group(value_type, current_value))
        SETTINGS[value_type] = current_value


def update_display():
    # Save a time value to track execution time

    # @todo check that getters and makers have the same keys
    # @todo use that list of keys here
    for e in ["LAYER", "BAR", "TAM_TAM"]:
        check_and_update(e)

    # Updates the display to show the frame group
    SETTINGS["OLED_DISPLAY"].refresh()


init()
