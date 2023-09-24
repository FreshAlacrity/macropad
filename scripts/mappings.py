import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from layers import list_layer_names

layer_names = list_layer_names()
mouse_speed = 5
sleep_time = 1000
current_layer = 1
selected_layer = current_layer
hold_duration = {}

# Set up abbreviations for different devices
kbd = Keyboard(usb_hid.devices)
m = Mouse(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
# alternatively: macropad.consumer_control.send
mouse_delta = {"x": 0, "y": 0}

# @todo mouse_angular_move(theta) that calls mouse_move(cos(theta), sin(theta))

def mouse_move(x, y):
    global mouse_delta
    speed = mouse_speed
    mouse_delta["x"] = mouse_delta["x"] + x * speed
    mouse_delta["y"] = mouse_delta["y"] + y * speed


def close_out():
    # Called at the end of the main loop
    global mouse_delta
    if mouse_delta["x"] != 0 or mouse_delta["y"] != 0:
        m.move(x=mouse_delta["x"], y=mouse_delta["y"])
        mouse_delta = {"x": 0, "y": 0}
        print("\n------------\n")


# Layer Actions
def current_layer_name():
    return layer_names[current_layer]


# @todo check that these work and wrap properly:
def layer_up():
    global current_layer
    current_layer = (current_layer + 1) % len(layer_names)
    layer(current_layer_name())


def layer_down():
    global current_layer
    current_layer = (current_layer - 1) % len(layer_names)
    layer(current_layer_name())


def layer_select(move=0):
    global selected_layer
    if move == 0:
        layer(layer_names[selected_layer])
    else:
        selected_layer = (selected_layer + move) % len(layer_names)
        print("\n\nTap for\n{}\n".format(layer_names[selected_layer]))


def layer(layer_name, inputs=0, time=sleep_time, entering=True):
    # @todo implement N inputs to leave the layer
    # @todo implement sleep/time to exit layer by timeout
    # @todo implement exit layer to parent
    global current_layer
    global selected_layer
    current_layer = layer_names.index(layer_name)
    selected_layer = current_layer
    print("\nCurrent Layer:\n", current_layer_name())


# @todo add arrow key support
key_actions = {
    "blank": {"action": (print, "Key Unassigned"), "hint": "Unassigned key action"},
    "l_up": {"action": layer_up, "hint": "Go up one layer"},
    "l_dn": {"action": layer_down, "hint": "Go down one layer"},
    "ls_up": {"action": (layer_select, 1), "hint": "Scroll up one layer"},
    "ls_dn": {"action": (layer_select, -1), "hint": "Scroll down one layer"},
    "ls_go": {"action": layer_select, "hint": "Move to the selected layer"},
    "vol_up": {
        "action": (cc.send, ConsumerControlCode.VOLUME_INCREMENT),
        "hint": "Turn up the sound volume",
    },
    "vol_dn": {
        "action": (cc.send, ConsumerControlCode.VOLUME_DECREMENT),
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
        "action": [0, 0, (mouse_move, (1, 0))],
        "hint": "Move the mouse right",
    },
    "m_ur": {
        "action": [0, 0, (mouse_move, (1, -1))],
        "hint": "Move the mouse up and right",
    },
    "m_lf": {
        "action": [0, 0, (mouse_move, (-1, 0))],
        "hint": "Move the mouse left",
    },
    "m_up": {
        "action": [0, 0, (mouse_move, (0, -1))],
        "hint": "Move the mouse up",
    },
    "m_dn": {
        "action": [0, 0, (mouse_move, (0, 1))],
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
            raise Exception(
                "Layer name collision:\n{} is already a key action".format(name)
            )
        else:
            key_actions[name] = {
                "action": (layer, name),
                "hint": "Switch to {} layer".format(name),
            }


add_layer_switch_actions()


def print_key_actions_list():
    # @todo sort by length = 0 and then alphabetically?
    print("Key actions:\n", ", ".join(key_actions.keys()))


def valid_action(action_name):
    if not isinstance(action_name, str):
        raise Exception("This action name is not a string: '{}'".format(action_name))
    elif action_name not in key_actions:
        raise Exception(
            "There is no action assigned to this name: '{}'".format(action_name)
        )
    elif "action" not in key_actions[action_name]:
        raise Exception(
            "There is no function assigned to action '{}'".format(action_name)
        )
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


def do_key_action(action_name, index=0):
    # Note: currently for index 0 is press, 1 is release, 2 is hold
    # macropad.play_tone(396, .2)
    indexes = ["press", "release", "hold"]
    print("Action received:", action_name, indexes[index])

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
    """
    # Currently erroring badly, @todo figure out why
    # Track duration of key hold (for things like acceleration)
    global hold_duration
    if index == 1:
        hold_duration[action_name] = 0
    elif index == 2:
        hold_duration[action_name] = hold_duration[action_name] + 1
    """

    if type(action) == type(do_key_action):
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


"""
all possible keycodes are listed here:
    https://usb.org/sites/default/files/hut1_21_0.pdf#page=83
note that keycodes are the names for key *positions* on a US keyboard

# As yet unsupported actions:

# Pause or resume playback.
cc.send(ConsumerControlCode.PLAY_PAUSE)

# Move the mouse diagonally to the upper left.
m.move(-100, -100, 0)

# Roll the mouse wheel away from the user one unit.
m.move(wheel=-1)

# Type control-x.
kbd.send(Keycode.CONTROL, Keycode.X)

# Press and hold the shifted '1' key to get '!' (exclamation mark).
kbd.press(Keycode.SHIFT, Keycode.ONE)
# Release the ONE key and send another report.
kbd.release(Keycode.ONE)
# Press shifted '2' to get '@'.
kbd.press(Keycode.TWO)
# Release all keys.
kbd.release_all()
"""


"""
"ConsumerControlCode": [
  'RECORD',
  'FAST_FORWARD',
  'REWIND',
  'SCAN_NEXT_TRACK',
  'SCAN_PREVIOUS_TRACK',
  'STOP',
  'EJECT',
  'PLAY_PAUSE',
  'MUTE',
  'VOLUME_DECREMENT',
  'VOLUME_INCREMENT',
  'BRIGHTNESS_DECREMENT',
  'BRIGHTNESS_INCREMENT'
],

"""
