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
    has_prefix = action_name[0 : len(prefix)] == prefix
    if has_prefix:
        # Trim the prefix off and re-check against aliases:
        action_name = identify(action_name[len(prefix) :])
    return action_name, has_prefix


def hid_action(action_name, action_type):
    """Sends the appropriate signal over the HID USB connection if a code is found in any of the HID directories
    Note: upper and lowercase letters need to be in the appropriate case in action_name to be sent correctly"""

    def check_dir(directory):
        return hasattr(directory, action_name.upper())

    is_uppercase = (
        len(action_name) == 1
        and action_name.isalpha()
        and not action_name == action_name.upper()
    )

    action_name, hold_action = check_prefix(action_name, "hold_")
    
    # Lists of accepted HID inputs and what function accepts those codes
    directories = (Keycode, ConsumerControlCode, Mouse)
    controllers = (Keyboard, ConsumerControl, Mouse)

    # Checks to see if any of the directories have the action_name in them
    built_in = [check_dir(x) for x in directories]

    if any(built_in):
        log("HERE")
        # From the HID input options, find the correct directory and controller
        controller = controllers[built_in.index(True)]
        directory = directories[built_in.index(True)]
        
        # Treat mouse clicks etc as held actions
        # (The mouse HID can't interpret send actions)
        if not hold_action and directory == Mouse:
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


@time_test("Key action")
def do_key_action(action_name, action_type):
    # Check against aliases:
    action_name = identify(action_name)

    # @todo detect macros here

    # Check for strings to write in directly and send them if found
    # Checked first to avoid accidentally parsing strings as keycodes
    action_name, write_this = check_prefix(action_name, "write_")
    if write_this:
        # Only write strings on press action, else ignore
        if action_type == "pressed":
            KeyboardLayoutUS(Keyboard(devices)).write(action_name)

    # Check for and do HID actions if available, else pass on to custom handler
    elif not hid_action(action_name, action_type):
        custom_action(action_name, action_type)


def init():
    # Just in case things have glitched out in the meantime,
    # release all held keys:
    Keyboard(devices).release_all()
    keycodes = [
        "ONE",
        "TWO",
        "THREE",
        "FOUR",
        "FIVE",
        "SIX",
        "SEVEN",
        "EIGHT",
        "NINE",
        "ZERO",
        "ENTER",
        "RETURN",
        "ESCAPE",
        "BACKSPACE",
        "TAB",
        "SPACEBAR",
        "SPACE",
        "MINUS",
        "EQUALS",
        "LEFT_BRACKET",
        "RIGHT_BRACKET",
        "BACKSLASH",
        "POUND",
        "SEMICOLON",
        "QUOTE",
        "GRAVE_ACCENT",
        "COMMA",
        "PERIOD",
        "FORWARD_SLASH",
        "CAPS_LOCK",
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "PRINT_SCREEN",
        "SCROLL_LOCK",
        "PAUSE",
        "INSERT",
        "HOME",
        "PAGE_UP",
        "DELETE",
        "END",
        "PAGE_DOWN",
        "RIGHT_ARROW",
        "LEFT_ARROW",
        "DOWN_ARROW",
        "UP_ARROW",
        "KEYPAD_NUMLOCK",
        "KEYPAD_FORWARD_SLASH",
        "KEYPAD_ASTERISK",
        "KEYPAD_MINUS",
        "KEYPAD_PLUS",
        "KEYPAD_ENTER",
        "KEYPAD_ONE",
        "KEYPAD_TWO",
        "KEYPAD_THREE",
        "KEYPAD_FOUR",
        "KEYPAD_FIVE",
        "KEYPAD_SIX",
        "KEYPAD_SEVEN",
        "KEYPAD_EIGHT",
        "KEYPAD_NINE",
        "KEYPAD_ZERO",
        "KEYPAD_PERIOD",
        "KEYPAD_BACKSLASH",
        "APPLICATION",
        "POWER",
        "KEYPAD_EQUALS",
        "F13",
        "F14",
        "F15",
        "F16",
        "F17",
        "F18",
        "F19",
        "F20",
        "F21",
        "F22",
        "F23",
        "F24",
        "LEFT_CONTROL",
        "CONTROL",
        "LEFT_SHIFT",
        "SHIFT",
        "LEFT_ALT",
        "ALT",
        "OPTION",
        "LEFT_GUI",
        "GUI",
        "WINDOWS",
        "COMMAND",
        "RIGHT_CONTROL",
        "RIGHT_SHIFT",
        "RIGHT_ALT",
        "RIGHT_GUI",
    ]
    # log(dir(Mouse))


init()
