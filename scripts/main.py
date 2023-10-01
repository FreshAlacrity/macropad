# Version 0.5

# CTRL+ALT+R > CTRL+C to enter REPL, CTRL+D to soft reboot

# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, no-value-for-parameter

import sys
from adafruit_macropad import MacroPad

sys.path.append("scripts")
from layers import get_action
from layers import get_layer_color
from layers import get_layer_pattern
from mappings import do_key_action
from mappings import current_layer_name
from mappings import final_actions
from display import update_display
from logger import log

# Stops reload on save:
# import supervisor
# supervisor.runtime.autoreload = False

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(90)

# Initial values
SETTINGS = {
    "INIT_ACTION": "Mouse",
    "TAP_DURATION": 0.1,  # TBD, in seconds?
    "SLEEP_AT": 100000
}


def input_action(current_key_num, index=0):
    """Retrieves and executes the action assigned to this key number on the current layer."""
    action = get_action(current_key_num, current_layer_name())
    do_key_action(action, index)
    unsleep()
    # @todo here - log the action somehow


def get_idle_time():
    return SETTINGS["idle_time"]


def update_LEDs(off=False):
    if off:
        for i in range(12):
            macropad.pixels[i] = (0, 0, 0)
    else:
        color = get_layer_color(current_layer_name())
        pattern = get_layer_pattern(current_layer_name())
        for i in pattern:
            macropad.pixels[i] = color


def sleep():
    update_LEDs(off=True)


def unsleep():
    SETTINGS["idle_time"] = 0


def close_out():
    """Wraps up any pending actions during the loop and updates the board LED display"""
    # If input has been received during this loop:
    if SETTINGS["idle_time"] >= SETTINGS["SLEEP_AT"]:
        sleep()
    else:
        if get_idle_time() == 0:
            final_actions()
            update_LEDs()
        update_display()


def init():
    # Set initial values for things that aren't set by the user
    SETTINGS["encoder_position"] = 0
    SETTINGS["keys_held"] = []
    unsleep()
    
    # Get things going!
    log("ARE WE BACK?! WE'RE BACK!")
    do_key_action(SETTINGS["INIT_ACTION"])
    close_out()


def check_keys():
    """Check for key presses send any input to action handler"""
    while macropad.keys.events:
        key_event = macropad.keys.events.get()
        if key_event:
            # Adds 3 to skip the rotary encoder inputs
            key_num = key_event.key_number + 3

            if key_event.pressed:
                input_action(key_num, 0)
                SETTINGS["keys_held"].append(key_num)

            if key_event.released:
                input_action(key_num, 1)
                SETTINGS["keys_held"].remove(key_num)

        if macropad.keys.events.overflowed:
            raise Exception("Key event overflow!")


def check_held_keys():
    for key in SETTINGS["keys_held"]:
        input_action(key, 2)


def check_rotary_encoder():
    """Check for rotary encoder input and send any input to action handler"""
    macropad.encoder_switch_debounced.update()
    current_position = macropad.encoder

    if macropad.encoder_switch_debounced.pressed:
        input_action(2, 0)

    # Clockwise turn detected
    if macropad.encoder > SETTINGS["encoder_position"]:
        input_action(0, 0)

    # Counterclockwise turn detected
    elif macropad.encoder < SETTINGS["encoder_position"]:
        input_action(1, 0)

    SETTINGS["encoder_position"] = current_position


# Main Loop
init()
while True:
    SETTINGS["idle_time"] += 1
    try:
        check_keys()
        check_held_keys()
        check_rotary_encoder()
        close_out()

    except Exception as err:
        log(f"Error: {err}, {type(err)}")
        raise
