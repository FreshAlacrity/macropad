# Version 0.4

# CTRL+ALT+R > CTRL+C to enter REPL, CTRL+D to soft reboot

# Based on: MacroPad HID keyboard and mouse demo,
# Unlicense 2021 by Kattni Rembor for Adafruit Induencoder_positiones

# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised


from adafruit_macropad import MacroPad
from layers import get_action
from layers import get_layer_color
from layers import get_layer_pattern
from mappings import do_key_action
from mappings import current_layer_name
from mappings import close_out
from timetest import time_test
from display import update_display
from logs import log

# Settings
INIT_ACTION = "Mouse"
SLEEP_AT = 100000
DEBUG = True

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(90)


# Initial values
SETTINGS = {
    "idle_time": 0,
    "encoder_position": 0,
    
    # Smaller numbers are faster (in loops not real time)
    "FRAME_RATE": 1
}
keys_held = []


# @todo get this working so it restores the USB connection
@time_test("File write attempt")
def file_write_attempt():
    try:
        modes = {
            "Read": "r",  # Errors if it doesn't exist
            "Append": "a",
            "Write": "w",  # Creates if it doesn't exist
            "Create": "x"  # Errors if it *does* exist
        }
        
        with open("/settings.toml", mode=modes["Append"], encoding="utf-8") as fp:
            while True:
                fp.write("HELLO WORLD! ")
                fp.flush()
    except OSError as _:
        # Typical error when the filesystem isn't writeable
        print("No files were written because the drive is in USB mode; reset with the button to change back (or uncomment out the drive-disabling code in boot.py)")

file_write_attempt()


log("ARE WE BACK?! WE'RE BACK!")

        
def input_action(current_key_num, index=0):
    """Retrieves and executes the action assigned to this key number on the current layer."""
    action = get_action(current_key_num, current_layer_name())
    do_key_action(action, index)
    # @todo here - log the action somehow


def get_idle_time():
    return SETTINGS["idle_time"]


def sleep():
    # @todo figure out why I can't import tam_tam
    for i in range(12):
        macropad.pixels[i] = (0, 0, 0)


def unsleep():
    SETTINGS["idle_time"] = 0


def update():
    frame_rate = SETTINGS["FRAME_RATE"]
    if get_idle_time() == 0:
        close_out()
        color = get_layer_color(current_layer_name())
        pattern = get_layer_pattern(current_layer_name())
        for i in pattern:
            macropad.pixels[i] = color
        update_display()
    elif get_idle_time() % frame_rate == 0:
        # Only updates the display every N frames
        update_display()


def init():
    print("\n\n\n\n\nBooting...\n")
    do_key_action(INIT_ACTION)
    update()

    # Loop forever so you can enjoy your image
    #while True:
        #pass

    # print("LAYER:", current_layer_name())


# Main Loop
init()
while True:
    SETTINGS["idle_time"] += 1
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
            if SETTINGS["idle_time"] == SLEEP_AT:
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
        if macropad.encoder > SETTINGS["encoder_position"]:
            input_action(0, 0)
            unsleep()

        # Counterclockwise turn detected
        elif macropad.encoder < SETTINGS["encoder_position"]:
            input_action(1, 0)
            unsleep()

        SETTINGS["encoder_position"] = current_position

        # Close out any pending actions (mouse movement etc)
        update()

    except Exception as err:
        print("Error: {}, {}".format(err, type(err)))
        raise
