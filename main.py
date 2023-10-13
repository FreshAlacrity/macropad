# Version 0.6

# CTRL+ALT+R > CTRL+C to enter REPL, CTRL+D to soft reboot

# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member, wrong-import-position, no-name-in-module

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, no-value-for-parameter

import sys
import supervisor
from adafruit_macropad import MacroPad

sys.path.append("scripts")
from layer_map import layer_action
from layer_actions import current_layer_name
from actions import do_key_action
from actions import final_actions
from actions import all_stop
from display import update_display
from display import swap_display
from time_test import time_test
from sounds import sound_init
from sounds import sound_check
from sounds import key_sound
from logger import log


SETTINGS = {
    "INIT_ACTION": "Scroll",
    "SLEEP_AT": 1000, #00,
    "ROTATION": 270,
    "inherited": {}
}

# Stops reload on save:
# Note that the serial monitor doesn't automatically reconnect after rebooting
#supervisor.runtime.autoreload = False

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(SETTINGS["ROTATION"])

@time_test("Input action")
def input_action(key_ref, action_type):
    
    # Retrieve the actions assigned to this key
    # Uses inherited values where present
    # Uses default values if no actions are found
    # @todo see if the rotary encoder is inheriting actions correctly
    # @todo check for and do uninherit
    if key_ref in SETTINGS["inherited"]:
        key_actions = SETTINGS["inherited"][key_ref]
    else:
        key_actions = layer_action(key_ref, current_layer_name())
    
    # Send them to be acted on
    for action in key_actions:
        do_key_action(action, action_type)
        
        # Check if this action can be inherited
        # @todo Remove "hold_" if present
        inheritable = (
            ("left", "right"),
            ("down", "up"),
            ("undo", "redo")
            )
        for pair in inheritable:
            for keyword in pair:
                if keyword in action:
                    log("Setting inheritance")
                    cw = action.replace(keyword, pair[0])
                    ccw = action.replace(keyword, pair[1])
                    SETTINGS["inherited"]["turn_up"] = (cw,)
                    SETTINGS["inherited"]["turn_down"] = (ccw,)
                    SETTINGS["inherited"]["turn_click"] = "uninherit"
                

    # Refresh the idle time counter
    unsleep()


def get_idle_time():
    return SETTINGS["idle_time"]


def sleep():
    log("Sleeping...")
    
    # Clear any inherited values
    # @todo see how this feels in practice
    SETTINGS["inherited"] = {}
    
    # @todo turn off the screen
    swap_display("off")
    
    # @todo slow down the main loop to once every tenth of a second-ish


def unsleep():
    SETTINGS["idle_time"] = 0
    swap_display("main")


@time_test("Close out")
def close_out():
    """Wraps up any pending actions during the loop and updates the board LED display"""
    if SETTINGS["idle_time"] == SETTINGS["SLEEP_AT"]:
        sleep()
    elif SETTINGS["idle_time"] > SETTINGS["SLEEP_AT"]:
        # @later Delay the next cycle?
        pass
    else:
        # If input has been received during this loop:
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
                key_sound(key_num)
                input_action(key_num, action_type="pressed")
                SETTINGS["keys_held"][key_num] = 0

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
        input_action("turn_down", "pressed")

    # Counterclockwise turn detected
    elif macropad.encoder < SETTINGS["encoder_position"]:
        input_action("turn_up", "pressed")

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
    
    # If the macropad was restarted for development reasons, play a tune
    when = (supervisor.RunReason.AUTO_RELOAD, supervisor.RunReason.REPL_RELOAD)
    play_tune = (supervisor.runtime.run_reason in when)
    sound_init(macropad, play_tune)
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
        log(f"Error: {err}, {type(err)}")
        raise
