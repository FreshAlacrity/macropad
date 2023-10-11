# Version 0.6

# CTRL+ALT+R > CTRL+C to enter REPL, CTRL+D to soft reboot

# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, no-value-for-parameter

import sys
from adafruit_macropad import MacroPad

sys.path.append("scripts")
from layer_map import get_key_layout
from layer_map import get_layer_map
from layer_actions import current_layer_name
from actions import do_key_action
from actions import final_actions
from display import update_display
from time_test import time_test
from logger import log


SETTINGS = {
    "INIT_ACTION": "Mouse",
    "TAP_DURATION": 0.1,  # TBD, in seconds?
    "SLEEP_AT": 100000,
    "ROTATION": 270,
    "LAYOUT": get_key_layout(),
    "LAYERS": get_layer_map()
}

# Stops reload on save:
# import supervisor
# supervisor.runtime.autoreload = False

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(SETTINGS["ROTATION"])

@time_test("Layer action")
def layer_action(key_names):
    layer_actions = SETTINGS["LAYERS"][current_layer_name()]["actions"]
    
    current_layer_actions = [layer_actions[x] for x in key_names if x in layer_actions]
    if current_layer_actions:
        return current_layer_actions
    else:
        # Reimplement falling back to lower layers @later
        layer_actions = SETTINGS["LAYERS"]["Default"]["actions"]
        return [layer_actions[x] for x in key_names if x in layer_actions]
    

def get_actions(key_num):
    key_names = SETTINGS["LAYOUT"][key_num]
    return layer_action(key_names)


def input_action(key_actions, action_type):

    # Send it off to be acted on
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


def close_out():
    """Wraps up any pending actions during the loop and updates the board LED display"""
    # If input has been received during this loop:
    if SETTINGS["idle_time"] >= SETTINGS["SLEEP_AT"]:
        sleep()
    else:
        if get_idle_time() == 0:
            final_actions()
        update_display()


def init():
    # Set initial values for things that aren't set by the user
    SETTINGS["encoder_position"] = 0
    SETTINGS["keys_held"] = []
    unsleep()

    # Get things going!
    log("ARE WE BACK?! WE'RE BACK!")
    do_key_action(SETTINGS["INIT_ACTION"], action_type="pressed")
    close_out()

    macropad.play_tone(196, 0.1)
    macropad.play_tone(220, 0.1)
    macropad.play_tone(246, 0.1)
    

@time_test("Key press/release check")
def check_keys():
    """Check for key presses send any input to action handler"""
    
    tones = [196, 220, 246, 262, 294, 330, 349, 392, 440, 494, 523, 587]
                
    while macropad.keys.events:
        key_event = macropad.keys.events.get()
        if key_event:
            key_num = key_event.key_number
            actions = get_actions(key_num)
            
            if key_event.pressed:
                input_action(actions, action_type="pressed")
                SETTINGS["keys_held"].append(key_num)
                macropad.play_tone(tones[key_num], 0.1)
                # macropad.start_tone(tones[key_num])

            if key_event.released:
                input_action(actions, action_type="released")
                SETTINGS["keys_held"].remove(key_num)
                #macropad.stop_tone()

        if macropad.keys.events.overflowed:
            raise Exception("Key event overflow!")

@time_test("Held keys check")
def check_held_keys():
    for key_num in SETTINGS["keys_held"]:
        input_action(get_actions(key_num), "held")

@time_test("Rotary encoder check")
def check_rotary_encoder():
    """Check for rotary encoder input and send any input to action handler"""
    macropad.encoder_switch_debounced.update()
    
    # Rotary encoder pressed
    if macropad.encoder_switch_debounced.pressed:
        input_action(layer_action(("turn_click",)), "pressed")

    # Clockwise turn detected
    if macropad.encoder > SETTINGS["encoder_position"]:
        input_action(layer_action(("turn_up",)), "pressed")

    # Counterclockwise turn detected
    elif macropad.encoder < SETTINGS["encoder_position"]:
        input_action(layer_action(("turn_down",)), "pressed")

    # Keep track of the current position to detect changes
    SETTINGS["encoder_position"] = macropad.encoder


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
