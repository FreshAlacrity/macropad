# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, pointless-string-statement, missing-function-docstring, no-value-for-parameter

import time
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.mouse import Mouse
from sounds import sound_check

# alternatively: macropad.consumer_control.send
from adafruit_hid.consumer_control_code import ConsumerControlCode
from usb_hid import devices
from aliases import identify
from aliases import check_prefix
from mouse_actions import update_mouse
from mouse_actions import mouse_action
from layer_actions import layer_action
from time_test import time_test
from logger import log


@time_test("Final actions")
def final_actions():
    # Called at the end of the main loop
    update_mouse()
    sound_check()

def log_key_actions_list():
    # @todo
    log("Key actions:\n", ", ".join([]))


def hid_action(action_name, action_type):
    """Sends the appropriate signal over the HID USB connection if a code is found in any of the HID directories
    Note: upper and lowercase letters need to be in the appropriate case in action_name to be sent correctly"""

    def check_dir(directory):
        return hasattr(directory, action_name.upper())

    is_uppercase = (
        len(action_name) == 1
        and action_name.isalpha()
        and action_name == action_name.upper()
    )

    action_name, hold_action = check_prefix(action_name, "hold_")
    
    # Lists of accepted HID inputs and what function accepts those codes
    directories = (Keycode, ConsumerControlCode, Mouse)
    controllers = (Keyboard, ConsumerControl, Mouse)

    # Checks to see if any of the directories have the action_name in them
    built_in = [check_dir(x) for x in directories]

    if any(built_in):
        log(f"Doing {action_name} {action_type}")
        
        # From the HID input options, find the correct directory and controller
        controller = controllers[built_in.index(True)]
        directory = directories[built_in.index(True)]
        
        # Always treat mouse clicks etc as held actions
        # (The mouse HID can't interpret "send" actions)
        if hold_action or directory == Mouse:
            hold_action = True

        # Get the code from the directory to send through the HID controller
        code = getattr(directory, action_name.upper())

        # Send the appropriate signal with the code through the controller
        if action_type == "pressed" and hold_action:
            # Tell the computer we've started to hold the key
            controller(devices).press(code)
        elif action_type == "released" and hold_action:
            # Tell the computer we've stopped holding the key
            controller(devices).release(code)
        elif action_type == "pressed" and not hold_action:
            # Regular keypress (sent immediately)
            if is_uppercase:
                controller(devices).send(Keycode.SHIFT, code)
            else:
                controller(devices).send(code)
                
        # Let the action handler know the action has been handled
        return True
    else:
        return False


# @todo test this
# Known issue: all single capitalized letters in macros will be made lowercase
def macro(string, action_type):
    def is_keycode(code): 
        return hasattr(Keycode, identify(code).upper())
            
    combos = string.split(" > ")
    for index, segment in enumerate(combos):
        # @todo figure out how to handle _hold actions
        codes = segment.split(" + ")
        
        if all([is_keycode(c) for c in codes]):
            # If it's just keycodes, send them together immediately
            if action_type == "pressed":
                keycodes = [getattr(Keycode, identify(c).upper()) for c in codes]
                Keyboard(devices).send(*keycodes)
        elif len(combos) == 1:
            # Treat the key as having multiple actions taken as normal
            # Reverse order for key release so they're stacked correctly
            if action_type == "released":
                codes.reverse()
            for code in codes:
                do_key_action(code, action_type)
                final_actions()  # Needed for mouse movement macros
        else:
            # Execute complete actions for this set
            for code in codes:
                do_key_action(code, "pressed")
                do_key_action(code, "held")
            codes.reverse()
            for code in codes:
                do_key_action(code, "released")
            final_actions()  # Needed for mouse movement macros
        if index < len(combos) - 1:
            # Allow time for execution but don't play a tone the whole time
            for _ in range(30):
                sound_check()
                time.sleep(0.01)


@time_test("Key action")
def do_key_action(action_name, action_type):
    # Check against aliases:
    action_name = identify(action_name)

    # @todo test macros
    if any([x in action_name for x in "+<"]):
        macro(action_name, action_type)
        return
    
    # _write is checked first to avoid parsing strings as keycodes
    action_name, write_this = check_prefix(action_name, "write_")
    
    if write_this:
        if action_type == "pressed":
            KeyboardLayoutUS(Keyboard(devices)).write(action_name)
    elif mouse_action(action_name, action_type):
        # mouse_action function checks + executes
        pass
    elif layer_action(action_name, action_type):
        # layer_action function checks + executes
        pass
    elif hid_action(action_name, action_type):
        # hid_action function checks + executes
        pass
    else: 
        # Not a recognized action at all
        log(f"ACTION UNKNOWN: {action_name}")


def all_stop():
    """Release all held keys (in case of error etc.)"""
    Keyboard(devices).release_all()


def init():
    # log(dir(Mouse))
    pass


init()
