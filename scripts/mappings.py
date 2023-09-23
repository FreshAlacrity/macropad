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

# Set up abbreviations for different devices
kbd = Keyboard(usb_hid.devices)
m = Mouse(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
# alternatively: macropad.consumer_control.send


# Layer Actions
def current_layer_name():
    return layer_names[current_layer]


# @todo check that these work and wrap properly:
def layer_up():
    global current_layer
    current_layer = len(layer_names) % (current_layer + 1)


def layer_down():
    global current_layer
    current_layer = len(layer_names) % (current_layer - 1)


def layer(layer_name, inputs=0, time=sleep_time, entering=True):
    # @todo implement N inputs to leave the layer
    # @todo implement sleep/time to exit layer by timeout
    # @todo implement exit layer to parent
    global current_layer
    current_layer = layer_names.index(layer_name)


# @todo add arrow key support
key_actions = {
    "blank": {"action": (print, "Key Unassigned"), "hint": "Unassigned key action"},
    "Mouse": {
        "action": (layer, "Mouse"),
        "hint": "Switch to Mouse layer (@todo auto add all layer names as key actions)",
    },
    "l_up": {"action": layer_up, "hint": "Go up one layer"},
    "l_dn": {"action": layer_down, "hint": "Go down one layer"},
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
    "m_rt": {"action": (m.move, {"x": +mouse_speed}), "hint": "Move the mouse right"},
    "m_lf": {"action": (m.move, {"x": -mouse_speed}), "hint": "Move the mouse left"},
    "m_up": {"action": (m.move, {"y": +mouse_speed}), "hint": "Move the mouse up"},
    "m_dn": {"action": (m.move, {"y": -mouse_speed}), "hint": "Move the mouse down"},
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


def print_key_actions_list():
    # @todo sort by length = 0 and then alphabetically?
    print("Key actions:\n", ", ".join(key_actions.keys()))


def do_key_action(action_name, index=0):
    # Note: currently for index: 0 is press, 1 is release
    # macropad.play_tone(396, .2)

    if not isinstance(action_name, str):
        raise Exception("This action name is not a string!")
    elif action_name not in key_actions:
        raise Exception(
            "There is no action assigned to this name: '{}".format(action_name)
        )
    elif "action" not in key_actions[action_name]:
        raise Exception(
            "There is no function assigned for this key action: '{}".format(action_name)
        )

    action = key_actions[action_name]["action"]
    print(key_actions[action_name]["hint"])
    if isinstance(key_actions[action_name], list):
        print("Press or release?")
        # If this key has a press and release action, get the correct one
        action = action[index]
    elif index == 1 and not isinstance(key_actions[action_name], list):
        print("Released with no release action")
        # This key has only a press action, do nothing on release
        return

    print("@debug here")

    if type(action) == type(do_key_action):
        print("Executing basic function")
        action()
    elif len(action) > 1:
        arg = action[1]
        if isinstance(arg, dict):
            print("Executing function with named arguments")
            action[0](**arg)
        if isinstance(arg, tuple):
            print("Executing function with tuple arguments")
            action[0](*arg)
        else:
            print("Executing function with other/string arguments")
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
