# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, pointless-string-statement, missing-function-docstring


import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from layers import get_layer_names  # type: ignore
from logger import log

SETTINGS = {
    "mouse_speed": 10,
    "current_layer": 0,
    "selected_layer": 0,
    "mouse_scoot": 2,
    "sleep_time": 1000
}
layer_names = get_layer_names()
MOUSE_DELTA = {"x": 0, "y": 0}
HOLD_DURATION = {}

# @todo Implement a standard way to do hold and release actions
# @todo Implement these for key actions too:
ALIASES = {
    "KEYCODE": {
        "WIN": "WINDOWS",
        "CTRL": "CONTROL",
        "PG_DN": "PAGE_DOWN",
        "PG_UP": "PAGE_UP",
        "L_TAB": "LEFT_TAB",
        "L_SHIFT": "LEFT_SHIFT"
    },
    "CONSUMER_CONTROL": {
        "VOL_DOWN": "VOLUME_DECREMENT",
        "VOLUME_DOWN": "VOLUME_DECREMENT",
        "VOL_DN": "VOLUME_DECREMENT",
        "VOL_UP": "VOLUME_DECREMENT",
        "VOLUME_UP": "VOLUME_DECREMENT",
        "FORWARD": "FAST_FORWARD",
        "FWD": "FAST_FORWARD",
        "NEXT": "SCAN_NEXT_TRACK",
        "PREV": "SCAN_PREVIOUS_TRACK",
        "PAUSE": "PLAY_PAUSE",
        "PLAY": "PLAY_PAUSE",
        "SCREEN_UP": "BRIGHTNESS_INCREMENT",
        "SCREEN_DN": "BRIGHTNESS_INCREMENT",
        "SCREEN_DOWN": "BRIGHTNESS_INCREMENT",
        "BRIGHTER": "BRIGHTNESS_INCREMENT",
        "DIMMER": "BRIGHTNESS_INCREMENT",
        "LT_UP": "BRIGHTNESS_DECREMENT",
        "LT_DN": "BRIGHTNESS_DECREMENT",
    },
}


# Set up abbreviations for different devices
kbd = Keyboard(usb_hid.devices)
us_layout = KeyboardLayoutUS(kbd)
m = Mouse(usb_hid.devices)
# alternatively: macropad.consumer_control.send


def mouse_move(x_delta, y_delta):
    speed = SETTINGS["mouse_speed"]
    log(f"X Delt: {x_delta} Y Delt: {y_delta} Speed: {speed}")
    MOUSE_DELTA["x"] = MOUSE_DELTA["x"] + x_delta * speed
    MOUSE_DELTA["y"] = MOUSE_DELTA["y"] + y_delta * speed


def final_actions():
    # Called at the end of the main loop
    if MOUSE_DELTA["x"] != 0 or MOUSE_DELTA["y"] != 0:
        m.move(x=MOUSE_DELTA["x"], y=MOUSE_DELTA["y"])
        MOUSE_DELTA["x"] = 0
        MOUSE_DELTA["y"] = 0
    # print("\n----------\n")


def sub_in_alias(string, alias_type):
    string = string.upper()
    if string in ALIASES[alias_type]:
        return ALIASES[alias_type][string.upper()]
    else:
        return string


def c_control(control_type):
    control_type = sub_in_alias(control_type, "CONSUMER_CONTROL")
    ConsumerControl(usb_hid.devices).send(getattr(ConsumerControlCode, control_type))


def get_keycode(string):
    return getattr(Keycode, string.upper())


def macro(string):
    def alias(string):
        return sub_in_alias(string, "KEYCODE")

    def check_code(string):
        return hasattr(Keycode, string.upper())

    combos = string.split(" > ")
    for index, segment in enumerate(combos):
        codes = segment.split(" + ")
        codes = list(map(alias, codes))
        if all(map(check_code, codes)):
            kbd.send(*tuple(map(get_keycode, codes)))
            if index < len(combos) - 1:
                time.sleep(0.3)  # allow time for execution
        else:
            us_layout.write(segment)


# Layer Actions
def current_layer_name():
    return layer_names[SETTINGS["current_layer"]]


# @todo check that these work and wrap properly:
def layer_up():
    SETTINGS["current_layer"] = (SETTINGS["current_layer"] + 1) % len(layer_names)
    layer(current_layer_name())


def layer_down():
    SETTINGS["current_layer"] = (SETTINGS["current_layer"] - 1) % len(layer_names)
    layer(current_layer_name())


def layer_select(move=0):
    if move == 0:
        layer(layer_names[SETTINGS["selected_layer"]])
    else:
        SETTINGS["selected_layer"] = (SETTINGS["selected_layer"] + move) % len(
            layer_names
        )
        print("\n\nTap for\n{}\n".format(layer_names[SETTINGS["selected_layer"]]))


def layer(layer_name):  # , inputs=0, time=sleep_time, entering=True):
    # @todo implement N inputs to leave the layer
    # @todo implement sleep/time to exit layer by timeout
    # @todo implement exit layer to parent
    SETTINGS["current_layer"] = layer_names.index(layer_name)
    SETTINGS["selected_layer"] = SETTINGS["current_layer"]
    log("Current Layer:", current_layer_name())


"""
To Add
# Pause or resume playback.


# Roll the mouse wheel away from the user one unit.
m.move(wheel=-1)

# Press and hold the shifted '1' key to get '!' (exclamation mark).
kbd.press(Keycode.SHIFT, Keycode.ONE)

# Release the ONE key and send another report.
kbd.release(Keycode.ONE)

# Press shifted '2' to get '@'.
kbd.press(Keycode.TWO)

# Release all keys.
kbd.release_all()

"""
key_actions = {
    "blank": {"action": (print, "Key Unassigned"), "hint": "Unassigned key action"},
    "drive_f": {
        "action": (macro, "WIN + E > CTRL > CTRL > CTRL + L > F: > ENTER"),
        "hint": "Open drive F (Windows only!)",
    },
    "l_up": {"action": layer_up, "hint": "Go up one layout layer (immediately)"},
    "l_dn": {"action": layer_down, "hint": "Go down one layout layer (immediately)"},
    "ls_up": {"action": (layer_select, 1), "hint": "Scroll up one layout layer"},
    "ls_dn": {"action": (layer_select, -1), "hint": "Scroll down one layout layer"},
    "ls_go": {"action": layer_select, "hint": "Move to the selected layout layer"},
    "vol_up": {
        "action": (c_control, "VOLUME_INCREMENT"),
        "hint": "Turn up the sound volume",
    },
    "vol_dn": {
        "action": (c_control, "VOLUME_DECREMENT"),
        "hint": "Turn down the sound volume",
    },
    "rt_click": {
        "action": (m.click, Mouse.RIGHT_BUTTON),
        "hint": "Click the right mouse button",
    },
    "lf_click": {
        "action": (m.click, Mouse.LEFT_BUTTON),
        "hint": "Click the left mouse button",
    },
    "md_click": {
        "action": (m.click, Mouse.MIDDLE_BUTTON),
        "hint": "Click the middle mouse button/scroll wheel",
    },
    "m_drag": {
        "action": (m.press, Mouse.LEFT_BUTTON),
        "hint": "Toggle on mouse drag (hold down left button)",
    },
    "m_stop": {
        "action": (m.release, Mouse.LEFT_BUTTON),
        "hint": "Toggle off mouse drag (release left button)",
    },
    "m_rt": {
        "action": [(mouse_move, (SETTINGS["mouse_scoot"], 0)), 0, (mouse_move, (1, 0))],
        "hint": "Move the mouse right",
    },
    "m_lf": {
        "action": [
            (mouse_move, (-SETTINGS["mouse_scoot"], 0)),
            0,
            (mouse_move, (-1, 0)),
        ],
        "hint": "Move the mouse left",
    },
    "m_up": {
        "action": [
            (mouse_move, (0, -SETTINGS["mouse_scoot"])),
            0,
            (mouse_move, (0, -1)),
        ],
        "hint": "Move the mouse up",
    },
    "m_dn": {
        "action": [(mouse_move, (0, SETTINGS["mouse_scoot"])), 0, (mouse_move, (0, 1))],
        "hint": "Move the mouse down",
    },
    "m_w": {
        "action": [(kbd.press, Keycode.W), (kbd.release, Keycode.W)],
        "hint": "Gamepad style W",
    },
    "m_a": {
        "action": [(kbd.press, Keycode.A), (kbd.release, Keycode.A)],
        "hint": "Gamepad style A",
    },
    "m_s": {
        "action": [(kbd.press, Keycode.S), (kbd.release, Keycode.S)],
        "hint": "Gamepad style S",
    },
    "m_d": {
        "action": [(kbd.press, Keycode.D), (kbd.release, Keycode.D)],
        "hint": "Gamepad style D",
    },
    "m_space": {
        "action": [(kbd.press, Keycode.SPACE), (kbd.release, Keycode.SPACE)],
        "hint": "Gamepad style space",
    },
    "m_shift": {
        "action": [(kbd.press, Keycode.LEFT_SHIFT), (kbd.release, Keycode.LEFT_SHIFT)],
        "hint": "Gamepad style left shift",
    },
}


def add_standard_key_actions():
    all_codes = dir(Keycode)
    for key in all_codes:
        if key[0] != "_":
            keycode = getattr(Keycode, key)
            # Handle basic letter inputs
            if len(key) == 1 and key.isalpha():
                key_actions[key.upper()] = {
                    "action": (kbd.send, (Keycode.SHIFT, keycode)),
                    "hint": "Uppercase input: '{}'".format(key),
                }
            key_actions[key.lower()] = {
                "action": (kbd.send, keycode),
                "hint": "Keyboard input: '{}'".format(key),
            }


add_standard_key_actions()


def add_layer_switch_actions():
    for name in layer_names:
        # @todo check that there's not an action collision
        if name in key_actions:
            raise Exception(f"Layer name collision:\n{name} is already a key action")
        else:
            key_actions[name] = {
                "action": (layer, name),
                "hint": f"Switch to {name} layer",
            }


add_layer_switch_actions()


def print_key_actions_list():
    # @todo sort by length = 0 and then alphabetically?
    print("Key actions:\n", ", ".join(key_actions.keys()))

    """
    Last Export:
    x, m_w, f20, f21, m_s, escape, f22, zero, f23, nine, end, f24, left_control, pound, backslash, blank, ls_dn, m_stop, f1, m_d, l_up, f2, m_a, semicolon, f3, five, f4, f5, f6, md_click, m_lf, m_dn, ls_up, space, f7, f8, f9, insert, tab, m_drag, z, two, E, D, G, lf_click, Z, F, A, C, rt_click, m_up, right_bracket, B, M, L, O, N, I, H, l_dn, ls_go, J, K, T, m_space, Q, P, S, R, U, V, W, minus, Y, X, page_up, page_down, keypad_forward_slash, keypad_asterisk, caps_lock, spacebar, down_arrow, keypad_plus, keypad_enter, keypad_two, keypad_three, m_shift, keypad_six, keypad_seven, keypad_eight, keypad_period, keypad_backslash, power, keypad_equals, application, f12, f13, f10, f11, f16, vol_dn, f14, f15, f17, control, backspace, home, three, enter, f18, f19, left_shift, left_alt, modifier_bit, alt, keypad_minus, option, keypad_four, left_gui, left_arrow, gui, windows, command, right_control, right_alt, right_gui, Mouse, Game, one, Layer Select, grave_accent, right_arrow, keypad_five, up_arrow, print_screen, shift, Default, vol_up, Minecraft, return, drive_f, keypad_nine, Cassette Beasts, keypad_zero, scroll_lock, delete, period, forward_slash, keypad_numlock, six, four, eight, right_shift, keypad_one, quote, e, d, g, f, a, c, b, comma, left_bracket, m, l, o, n, i, h, k, j, u, m_rt, w, v, q, pause, p, s, equals, r, t, seven, y
    """


def valid_action(action_name):
    if not isinstance(action_name, str):
        raise Exception(f"This action name is not a string: '{action_name}'")
    elif action_name not in key_actions:
        raise Exception(f"There is no action assigned to this name: '{action_name}'")
    elif "action" not in key_actions[action_name]:
        raise Exception(f"There is no function assigned to action '{action_name}'")
    return True


def valid_index(action, index):
    if index >= len(action):
        # print("Index outside of list of specified actions")
        return False
    elif action[index] == 0:
        # print("No action specified for this index")
        return False
    else:
        return True


def track_hold(action_name, index):
    global HOLD_DURATION  # pylint: disable=global-variable-not-assigned
    if index == 1:
        HOLD_DURATION[action_name] = 0
    elif index == 2:
        if action_name in HOLD_DURATION:
            HOLD_DURATION[action_name] = HOLD_DURATION[action_name] + 1
        else:
            HOLD_DURATION[action_name] = 1


def do_key_action(action_name, action_type):
    # Intermediate support:
    index = ["pressed", "released", "held"].index(action_type)
    # macropad.play_tone(396, .2)
    # action_type = ["press", "release", "hold"][index]
    # print("\nAction received: '{}'\nType: {}\n".format(action_name, action_type))

    if not valid_action(action_name):
        return
    else:
        action = key_actions[action_name]["action"]
        # print(key_actions[action_name]["hint"])
    # Handle case: only press action specified
    if not isinstance(action, list):
        action = [action]
    if valid_index(action, index):
        action = action[index]
    else:
        return

    track_hold(action_name, index)
    # @here
    if callable(action):
        # print("Executing basic function")
        action()
    elif len(action) > 1:
        arg = action[1]
        if isinstance(arg, dict):
            # print("Executing function with named arguments")
            action[0](**arg)
        if isinstance(arg, tuple):
            # print("Executing function with tuple arguments")
            action[0](*arg)
        else:
            # print("Executing function with other/string arguments")
            action[0](arg)
    else:
        print("Error - key input not a function")
