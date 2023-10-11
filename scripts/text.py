# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, no-value-for-parameter

import board
import terminalio
from adafruit_display_text import label
from time_test import time_test


DISPLAY_SETTINGS = {
    "FONT": terminalio.FONT,
    "OLED_DISPLAY": board.DISPLAY,
    # @todo check these
    "CHAR_WIDTH": 5,
    "CHAR_HEIGHT": 12 
}

@time_test("String bitmap")
def make_string_bitmap(string, sx=0, sy=0):
    font = DISPLAY_SETTINGS["FONT"]
    
    char_height = DISPLAY_SETTINGS["CHAR_HEIGHT"]
    
    
    # Create the text label
    text_area = label.Label(font, text=string, color=0xFFFFFF)
    
    # Set the location
    text_area.x = sx
    text_area.y = sy + char_height // 2

    return(text_area)


def centered_text(string, sy=10):
    char_width = DISPLAY_SETTINGS["CHAR_WIDTH"]
    width = len(string) * char_width
    sx = (DISPLAY_SETTINGS["OLED_DISPLAY"].width - width) // 2
    bitmap = make_string_bitmap(string, sx, sy)
    return bitmap


def multi_line_text(string, sx, sy):
    # see adafruit_display_text.wrap_text_to_lines
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
    return make_string_bitmap("\n".join(lines), sx, sy)


def new_layer_bitmap(layer_name):
    vertical_offset = DISPLAY_SETTINGS["OLED_DISPLAY"].height - DISPLAY_SETTINGS["CHAR_HEIGHT"]
    return multi_line_text(layer_name, 0, vertical_offset)