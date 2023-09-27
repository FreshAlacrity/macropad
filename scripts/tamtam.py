# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

import board
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from timetest import new_test
from timetest import test_end

SETTINGS = {
    "FONT_DIR": "fonts/",
    "FONT_FILE": "ucs-fonts/7x13.bdf",
    "OLED_DISPLAY": board.DISPLAY
}

# @todo condense these more
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
        "υ _ υ",
        "n _ n",
        "O ω O",
        "ὲ ◡ έ",
        "ὶ ◡ ί",
        "Ξ ◡ Ξ",
        "' o '",
        "∩ _ ∩",
        "- ◡ O",  # 34
        "c(_)  ",
        "⚆ _ ⚆",
        "# _ #"
    ]


def font_setup():
    """Gets the font dimensions from the filename"""        
    font_dimensions = SETTINGS["FONT_FILE"].split("/")
    font_dimensions = font_dimensions[len(font_dimensions) - 1]
    font_dimensions = font_dimensions.split("x")
    SETTINGS["CHAR_WIDTH"] = int(font_dimensions[0])
    font_dimensions = font_dimensions[1].split(".")
    SETTINGS["CHAR_HEIGHT"] = int(font_dimensions[0])
    print(SETTINGS["CHAR_WIDTH"], SETTINGS["CHAR_HEIGHT"])
font_setup()

def make_string_bitmap(string, sx=0, sy=0):
    font = bitmap_font.load_font(f"{SETTINGS['FONT_DIR']}{SETTINGS['FONT_FILE']}")
    
    char_height = SETTINGS["CHAR_HEIGHT"]
    
    time_test = new_test(f"String bitmap of '{string}'")
    
    # Create the text label
    text_area = label.Label(font, text=string, color=0xFFFFFF)

    test_end(time_test)
    
    # Set the location
    text_area.x = sx
    text_area.y = sy + char_height // 2

    return(text_area)

def centered_text(string, sy=10):
    char_width = SETTINGS["CHAR_WIDTH"]
    width = len(string) * char_width
    sx = (SETTINGS["OLED_DISPLAY"].width - width) // 2
    bitmap = make_string_bitmap(string, sx, sy)
    return bitmap

def current_face_sprite(face_string, sy):
    return centered_text(face_string, sy)

def current_face_string(elapsed_time):
    """Returns a string value 5 characters long containing the current tamtam face expression"""
    mood = "all"
    indexes = tam_tam_faces(mood)
    frames_elapsed = int(elapsed_time * 30 / (len(indexes) - 1))
    frame = frames_elapsed % len(indexes)
    current_face = all_faces()[indexes[frame]]
    return current_face

def unique_chars():
    # Get all characters in all faces other than spaces
    string = ''.join(all_faces()).replace(' ', '')
    
    # Split and deduplicate the list of characters
    chars = list(dict.fromkeys(list(string)))
    return chars

# @todo make a sprite sheet with https://docs.circuitpython.org/projects/bitmapsaver/en/latest/api.html

def tam_tam_faces(mood):
    faces = {
        "all": {
            "faces": range(len(all_faces())),
            "frames": 4,
        },
        "egg": {
            "faces": [0, 1], 
            "frames": 10
        },
        "happy": {
            "faces": [3, 4],
            "frames": 4,
        },
        "neutral": {
            "faces": [5, 7, 5, 8, 5, 6],
            "frames": 6,
        },
        "tea": {
            "faces": [2, 35],
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
            "faces": [26, 5, 6, 16],
            "frames": 3,
        },
        "tired": {
            "faces": [25, 26],
            "frames": 3,
        },
        "sneaky": {
            "faces": [15, 28, 29, 30, 27],
            "frames": 4,
        },
        "random": {
            "faces": [31, 32, 33, 34, 27],
            "frames": 1,
        },
    }
    return faces[mood]["faces"]
