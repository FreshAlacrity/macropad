# Version 0.3

# Mu: CTRL + C > any key to enter REPL, CTRL + D to exit

# Based on: MacroPad HID keyboard and mouse demo,
# Unlicense 2021 by Kattni Rembor for Adafruit Induencoder_positiones

# Since the workspace setting isn't working:
# pyright: reportMissingImports=false

# pylint: disable=broad-exception-raised, global-statement

import time
import board
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_macropad import MacroPad
from layers import get_action
from layers import get_layer_color
from layers import get_layer_pattern
from mappings import do_key_action
from mappings import current_layer_name
from mappings import close_out

# Settings
init_action = "Mouse"
sleep_at = 100000
font_file = "fonts/LeagueSpartan-Bold-16.bdf"

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(90)

# Initial values
start_time = time.monotonic()
idle_time = 0
encoder_position = 0
keys_held = []


def show_glyph():
    # see https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font/blob/main/examples/bitmap_font_label_simpletest.py

    # use built in display (MagTag, PyPortal, PyGamer, PyBadge, CLUE, etc.)
    # see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
    # https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus

    # Set text, font, and color
    text = "HELLO\nWORLD"
    font = bitmap_font.load_font(font_file)

    # Create the text label
    text_area = label.Label(font, text=text, color=0xFFFFFF)

    # Set the location
    text_area.x = 0
    text_area.y = 10

    # Show it
    board.DISPLAY.show(text_area) # pylint: disable=no-member
    print("here")


def input_action(current_key_num, index=0):
    """Retrieves and executes the action assigned to this key number on the current layer."""
    action = get_action(current_key_num, current_layer_name())
    # print("KEY:", key_num, ["down", "up", "hold"][index])
    # print("ACTION:", action)
    do_key_action(action, index)
    # @todo log the action somehow


def tam_tam(face="happy"):
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
            "faces": ["Ξ ◡ Ξ", "◑ ◡ ◐", "' o '", "∩ _ ∩", "- ◡ ◕"],
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
    # Refresh the display only every N cycles
    if idle_time % 100 == 0:
        mood_data = faces[face]
        frames_elapsed = int(
            (time.monotonic() - start_time) * 5 / (mood_data["frames"] - 1)
        )
        frame = frames_elapsed % len(mood_data["faces"])
        current_face = mood_data["faces"][frame]
        print(f"\n\n{frames_elapsed}\n{frame}\n\n{current_face}\n\n\n||||||||||")


def sleep():
    tam_tam("asleep")
    for i in range(12):
        macropad.pixels[i] = (0, 0, 0)


def unsleep():
    global idle_time
    idle_time = 0


def update():
    if idle_time == 0:
        close_out()
        color = get_layer_color(current_layer_name())
        pattern = get_layer_pattern(current_layer_name())
        for i in pattern:
            macropad.pixels[i] = color
    else:
        tam_tam()


def init():
    print("\n\n\n\n\nBooting...\n")
    do_key_action(init_action)
    update()
    # show_glyph()
    # print("LAYER:", current_layer_name())


# Main Loop
init()
while True:
    idle_time += 1
    try:
        while macropad.keys.events:
            key_event = macropad.keys.events.get()
            if key_event:
                # Adds 3 to skip the rotary encoder inputs
                key_num = key_event.key_number + 3

                if key_event.pressed:
                    input_action(key_num, 0)
                    keys_held.append(key_num)

                if key_event.released:
                    input_action(key_num, 1)
                    keys_held.remove(key_num)

            unsleep()

        if macropad.keys.events.overflowed:
            raise Exception("Key event overflow!")
        # else:
        #    print(keys_held)

        if len(keys_held) == 0:
            if idle_time == sleep_at:
                sleep()

        else:
            for key in keys_held:
                input_action(key, 2)
            unsleep()

        # Check for rotary encoder input
        macropad.encoder_switch_debounced.update()
        current_position = macropad.encoder

        if macropad.encoder_switch_debounced.pressed:
            input_action(2, 0)
            unsleep()

        # Clockwise turn detected
        if macropad.encoder > encoder_position:
            input_action(1, 0)
            unsleep()

        # Counterclockwise turn detected
        elif macropad.encoder < encoder_position:
            input_action(0, 0)
            unsleep()

        encoder_position = current_position

        # Close out any pending actions (mouse movement etc)
        update()

    except Exception as err:
        print("Error: {}, {}".format(err, type(err)))
        raise
