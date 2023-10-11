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

# alternatively: macropad.consumer_control.send
from adafruit_hid.consumer_control_code import ConsumerControlCode
from usb_hid import devices
from aliases import identify
from mouse_actions import update_mouse
from custom_actions import custom_action
from time_test import time_test
from logger import log


@time_test("Final actions")
def final_actions():
    # Called at the end of the main loop
    update_mouse()


def log_key_actions_list():
    # @todo
    log("Key actions:\n", ", ".join([]))


# @todo fix this so it breaks things into actions instead
def macro(string):
    combos = string.split(" > ")
    for index, segment in enumerate(combos):
        codes = segment.split(" + ")
        for code in codes:
            # @todo figure out which should be press and which should be held and use the "hold_" prefix to do that
            do_key_action(code, "pressed")
            # @todo things here
            if index < len(combos) - 1:
                time.sleep(0.3)  # allow time for execution


def check_prefix(action_name, prefix):
    test = action_name[0 : len(prefix)] == prefix
    if test:
        action_name = identify(action_name[len(prefix)])
    return action_name, test

@time_test("Key action")
def do_key_action(action_name, action_type):
    def uppercase_letter():
        return (
            len(action_name) == 1
            and action_name.isalpha()
            and not action_name == action_name.upper()
        )

    # @todo detect macros here
    action_name = identify(action_name)

    if not action_type == "pressed":
        # Detect and implement held keys:
        action_name, hold = check_prefix(action_name, "hold_")
        if hold:
            # Handle keyboard codes
            if action_name in dir(Keycode):
                keycode = getattr(Keycode, action_name.upper())
                if action_type == "pressed":
                    Keyboard(devices).press(keycode)
                elif action_type == "released":
                    Keyboard(devices).release(keycode)
        else:            
            # Handle mouse clicks
            if action_name in dir(Mouse):
                keycode = getattr(Mouse, action_name.upper())
                if action_type == "pressed":
                    Mouse(devices).press(keycode)
                elif action_type == "released":
                    Mouse(devices).release(keycode)
                    
            # Handle any custom actions
            else:
                # Handle all other input types:
                custom_action(action_name, action_type)
    if action_type == "pressed":
         
        # Detect and handle string input:
        action_name, write_this = check_prefix(action_name, "write_")
        if write_this:
            KeyboardLayoutUS(Keyboard(devices)).write(action_name)

        # Detect and handle uppercase letters:
        elif uppercase_letter():
            keycode = getattr(Keycode, action_name.upper())
            Keyboard(devices).send(Keycode.SHIFT, keycode)

        # Detect and handle plain keycodes:
        elif hasattr(Keycode, action_name.upper()):
            keycode = getattr(Keycode, action_name.upper())
            Keyboard(devices).send(keycode)

        # Detect and handle consumer control codes:
        elif hasattr(ConsumerControlCode, action_name.upper()):
            cc_code = getattr(ConsumerControlCode, action_name.upper())
            ConsumerControl(devices).send(cc_code)

        # Detect and handle standard mouse actions
        elif hasattr(Mouse, action_name.upper()):
            Mouse(devices).click(getattr(Mouse, action_name.upper()))

        # Handle all other input types:
        else:
            custom_action(action_name, action_type)


def init():
    # Just in case things have glitched out in the meantime,
    # Release all held keys:
    Keyboard(devices).release_all()


init()
