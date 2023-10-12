# Version 0.6

# CTRL+ALT+R > CTRL+C to enter REPL, CTRL+D to soft reboot

# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member, wrong-import-position, no-name-in-module

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, no-value-for-parameter

import sys
# from supervisor import runtime
from adafruit_macropad import MacroPad

sys.path.append("scripts")
from layer_map import layer_action
from layer_actions import current_layer_name
from actions import do_key_action
from actions import final_actions
from actions import all_stop
from display import update_display
from time_test import time_test
from sounds import sound_init
from sounds import sound_check
from sounds import key_sound
from logger import log


SETTINGS = {
    "INIT_ACTION": "Arrows",
    "SLEEP_AT": 100000,
    "ROTATION": 270
}

# Stops reload on save:
# Note that the serial monitor doesn't automatically reconnect after rebooting
#runtime.autoreload = False

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(SETTINGS["ROTATION"])


@time_test("Input action")
def input_action(key_ref, action_type):
    
    # Retrieve the actions assigned to this key
    # Uses default values if no actions are found
    key_actions = layer_action(key_ref, current_layer_name())
    
    # Send them to be acted on
    for action in key_actions:
        do_key_action(action, action_type)

    # Refresh the idle time counter
    unsleep()


def get_idle_time():
    return SETTINGS["idle_time"]


def sleep():
    # @todo Set the timer to 0
    # @todo turn off the screen
    # @todo slow down the main loop to once every tenth of a second-ish
    pass


def unsleep():
    SETTINGS["idle_time"] = 0


@time_test("Close out")
def close_out():
    """Wraps up any pending actions during the loop and updates the board LED display"""
    # If input has been received during this loop:
    if SETTINGS["idle_time"] >= SETTINGS["SLEEP_AT"]:
        sleep()
    else:
        if get_idle_time() == 0:
            final_actions()
        update_display()


@time_test("Key press/release check")
def check_keys():
    """Check for key presses send any input to action handler"""

    while macropad.keys.events:
        key_event = macropad.keys.events.get()
        if key_event:
            key_num = key_event.key_number
            
            if key_event.pressed:
                input_action(key_num, action_type="pressed")
                SETTINGS["keys_held"][key_num] = 0
                key_sound(key_num)

            if key_event.released:
                input_action(key_num, action_type="released")
                del SETTINGS["keys_held"][key_num]

        if macropad.keys.events.overflowed:
            raise Exception("Key event overflow!")


@time_test("Held keys check")
def check_held_keys():
    for key_num in SETTINGS["keys_held"].keys():
        input_action(key_num, action_type="held")
        # SETTINGS["keys_held"][key_num] += 1


@time_test("Rotary encoder check")
def check_rotary_encoder():
    """Check for rotary encoder input and send any input to action handler"""
    macropad.encoder_switch_debounced.update()

    # Rotary encoder pressed
    if macropad.encoder_switch_debounced.pressed:
        input_action("turn_click", "pressed")

    # Clockwise turn detected
    if macropad.encoder > SETTINGS["encoder_position"]:
        input_action("turn_up", "pressed")

    # Counterclockwise turn detected
    elif macropad.encoder < SETTINGS["encoder_position"]:
        input_action("turn_down", "pressed")

    # Keep track of the current position to detect changes
    SETTINGS["encoder_position"] = macropad.encoder


# @time_test("Main init")
def init():
    # Set initial values for things that aren't set by the user
    SETTINGS["encoder_position"] = 0
    SETTINGS["keys_held"] = {}
    unsleep()

    # Get things going!
    log("ARE WE BACK?! WE'RE BACK!")
    do_key_action(SETTINGS["INIT_ACTION"], action_type="pressed")
    close_out()

    sound_init(macropad)
init()


# Main Loop
while True:
    SETTINGS["idle_time"] += 1
    try:
        check_keys()
        check_held_keys()
        check_rotary_encoder()
        sound_check()
        close_out()

    except Exception as err:
        all_stop()
        sleep()
        log(f"Error: {err}, {type(err)}")
        raise
