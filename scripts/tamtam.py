# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error

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

START_TIME = time.monotonic()
faces = {
    "egg": {
        "faces": ["  o  ", "  O  "],
        "frames": 10,
    },
    "tea": {
        "faces": ["∩ _ ∩", "c(_)"],
        "frames": 6,
    },
    "eating": {
        "faces": ["∩ _ ∩", "- w -", "- θ -"],
        "frames": 6,
    },
    "sick": {
        "faces": ["X _ X", "> _ <"],
        "frames": 6,
    },
    "asleep": {
        "faces": ["- _ -", "- _ -", "- o -", "...zZzzZZ"],
        "frames": 21,
    },
    "sad": {
        "faces": ["υ _ υ", "џ _ џ", "ὺ _ ύ"],
        "frames": 6,
    },
    "scared": {
        "faces": ["° _ °", "O Д O", "; Д ;"],
        "frames": 4,
    },
    "angry": {
        "faces": ["¬ _ ¬", "ὸ _ ό", "◣ _ ◢"],
        "frames": 4,
    },
    "sneaky": {
        "faces": ["¬ ◡ ¬", "◕ ω ◕", "ὲ ◡ έ", "ὶ ◡ ί"],
        "frames": 4,
    },
    "hungry": {
        "faces": ["τ _ τ", "> _ <"],
        "frames": 4,
    },
    "tired": {
        "faces": ["v _ v", "υ _ υ", "n _ n"],
        "frames": 3,
    },
    "random": {
        "faces": ["Ξ ◡ Ξ", "' o '", "∩ _ ∩", "- ◡ ◕"],
        "frames": 1,
    },
    "happy": {
        "faces": ["◕ ◡ ◕", "- ◡ -"],
        "frames": 4,
    },
    "neutral": {
        "faces": ["• _ •", "> _ >", "• _ •", "< _ <", "• _ •", "- _ -"],
        "frames": 6,
    },
}

    
def add_all_faces():
    def deduplicate_list(x):
        return list(dict.fromkeys(x))

    new = []
    for _, data in faces.items():
        for face in data["faces"]:
            new.append(face)
            
    new = deduplicate_list(new)
    faces["all"] = { "faces": new, "frames": 10 }

add_all_faces()

def get_tam_tam_faces():
    """Returns the dictionary of faces for all possible tamtam moods"""
    return faces


def display_bitmap_text():
    # WARNING: VERY SLOW!
    # see https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font/blob/main/examples/bitmap_font_label_simpletest.py

    # use built in display (MagTag, PyPortal, PyGamer, PyBadge, CLUE, etc.)
    # see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
    # https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
    
    # @todo how to detect unsupported characters
    
    # @todo do automatic linebreaks according to character width
    FONT_DIR = "fonts/"
    FONTS = [
            "LeagueSpartan-Bold-16.bdf", 
            "ucs-fonts/4x6.bdf", 
            "uw-ttyp0/t0-12.bdf", 
            "uw-ttyp0/t0-12b.bdf"
        ]
    FONT_FILE_PATH = f"{FONT_DIR}{FONTS[1]}"
    # WIDTH = 4
    font = bitmap_font.load_font(FONT_FILE_PATH)
    
    text = """ὺ _ ύ τ _ τ
• _ • ὸ _ ό
- ◡ ◕ ◣ _ ◢
ὲ ◡ έ ὶ ◡ ί
- θ - ∩ _ ∩
Ξ ◡ Ξ ¬ _ ¬ 
◑ ◡ ◐ ◕ ω ◕
- ◡ - ; Д ;
° _ ° υ _ υ
џ _ џ ¬ ◡ ¬ 
"""

    # log(f"Bitmap Output:\n{text}")
    
    # Create the text label
    text_area = label.Label(font, text=text, color=0xFFFFFF)

    # Set the location
    text_area.x = 0
    text_area.y = 10

    # Show it
    board.DISPLAY.show(text_area) # pylint: disable=no-member


# DISPLAY IO STUFF
display = board.DISPLAY
display.auto_refresh = False

# Create a bitmap with two colors
bitmap = displayio.Bitmap(display.width, display.height, 2)

# Create a two color palette
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xffffff

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.show(group)

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
    draw_pixel()
    draw_rect(10, 5, 40, 10)
    display.refresh()


def tam_tam(face="happy"):
    mood_data = faces[face]
    frames_elapsed = int(
        (time.monotonic() - START_TIME) * 5 / (mood_data["frames"] - 1)
    )
    frame = frames_elapsed % len(mood_data["faces"])
    current_face = mood_data["faces"][frame]
    print(f"\n\n\n\n{frames_elapsed}\n{frame}\n\n{current_face}\n\n\n||||||||||")
    # why isn't this putting the |||| on the last row? nothing shows there?!
    