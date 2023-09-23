import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

mouse_speed = 5

# Set up abbreviations for different devices
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
# alternatively: macropad.consumer_control.send
m = Mouse(usb_hid.devices)


def nothing():
    print("no action")

"""
# Examples
def key_combination():
    macropad.keyboard.press(macropad.Keycode.SHIFT, macropad.Keycode.B)
    macropad.keyboard.release_all()
"""


# Layer Actions
def layer_up():
    global current_layer
    current_layer = current_layer + 1


def layer_down():
    global current_layer
    current_layer = current_layer - 1


# @todo add arrow key support
key_actions = {
    "m_w": [(kbd.press, Keycode.W), (kbd.release, Keycode.W)],
    "m_a": [(kbd.press, Keycode.A), (kbd.release, Keycode.A)],
    "m_s": [(kbd.press, Keycode.S), (kbd.release, Keycode.S)],
    "m_d": [(kbd.press, Keycode.D), (kbd.release, Keycode.D)],
    "blank": (print, "Key Unassigned"),
    "vol_up": (cc.send, ConsumerControlCode.VOLUME_INCREMENT),
    "vol_dn": (cc.send, ConsumerControlCode.VOLUME_DECREMENT),
    "r_click": (m.click, Mouse.RIGHT_BUTTON),
    "m_up": (m.move, {"y": -mouse_speed}),
    "m_rt": (m.move, {"x": +mouse_speed}),
    "m_lg": (m.move, {"x": -mouse_speed}),
    "m_dn": (m.move, {"y": +mouse_speed}),
    "l_up": layer_up,
    "l_dn": layer_down,
}

def do_key_action(action_name, index):
    # Note: currently for index: 0 is press, 1 is release
    # macropad.play_tone(396, .2)

    if not isinstance(action_name, str):
        raise Exception("This action name is not a string!")
    if len(action_name) == 1 and action_name.isalpha():
        # Handle basic letter input
        key_name = getattr(Keycode, action_name.upper())
        if index == 0:
            if action_name.islower():
                kbd.send(key_name)
            else:
                kbd.send(Keycode.SHIFT, key_name)
        return
    elif action_name not in key_actions:
        raise Exception(
            "There is no action assigned to this name: '{}".format(action_name)
        )

    action = key_actions[action_name]
    if isinstance(key_actions[action_name], list):
        action = action[index]
    elif index == 1 and not isinstance(key_actions[action_name], list):
        # This key has only a press action, do nothing on release
        return

    if type(action) == type(do_key_action):
        #  print("Executing function")
        action()
    elif len(action) > 1:
        arg = action[1]
        if isinstance(arg, dict):
            action[0](**arg)
        else:
            action[0](arg)

    else:
        print("Error - key input not a function")

"""



# Pause or resume playback.
cc.send(ConsumerControlCode.PLAY_PAUSE)


# Click the left mouse button.
m.click(Mouse.LEFT_BUTTON)

# Move the mouse diagonally to the upper left.
m.move(-100, -100, 0)

# Roll the mouse wheel away from the user one unit.
# Amount scrolled depends on the host.
m.move(0, 0, -1)

# Keyword arguments may also be used. Omitted arguments default to 0.
m.move(x=-100, y=-100)
m.move(wheel=-1)

# Move the mouse while holding down the left button. (click-drag).
m.press(Mouse.LEFT_BUTTON)
m.move(x=50, y=20)
m.release_all()       # or m.release(Mouse.LEFT_BUTTON)


# Type capital 'A'.
kbd.send(Keycode.SHIFT, Keycode.A)

# Type control-x.
kbd.send(Keycode.CONTROL, Keycode.X)

# You can also control press and release actions separately.
kbd.press(Keycode.CONTROL, Keycode.X)
kbd.release_all()

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
allKeys = {
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
    "Keycode": [
        'C',
        'M',
        'A',
        'B',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z',
        'ONE',
        'TWO',
        'THREE',
        'FOUR',
        'FIVE',
        'SIX',
        'SEVEN',
        'EIGHT',
        'NINE',
        'ZERO',
        'ENTER',
        'RETURN',
        'ESCAPE',
        'BACKSPACE',
        'TAB',
        'SPACEBAR',
        'SPACE',
        'MINUS',
        'EQUALS',
        'LEFT_BRACKET',
        'RIGHT_BRACKET',
        'BACKSLASH',
        'POUND',
        'SEMICOLON',
        'QUOTE',
        'GRAVE_ACCENT',
        'COMMA',
        'PERIOD',
        'FORWARD_SLASH',
        'CAPS_LOCK',
        'F1',
        'F2',
        'F3',
        'F4',
        'F5',
        'F6',
        'F7',
        'F8',
        'F9',
        'F10',
        'F11',
        'F12',
        'PRINT_SCREEN',
        'SCROLL_LOCK',
        'PAUSE',
        'INSERT',
        'HOME',
        'PAGE_UP',
        'DELETE',
        'END',
        'PAGE_DOWN',
        'RIGHT_ARROW',
        'LEFT_ARROW',
        'DOWN_ARROW',
        'UP_ARROW',
        'KEYPAD_NUMLOCK',
        'KEYPAD_FORWARD_SLASH',
        'KEYPAD_ASTERISK',
        'KEYPAD_MINUS',
        'KEYPAD_PLUS',
        'KEYPAD_ENTER',
        'KEYPAD_ONE',
        'KEYPAD_TWO',
        'KEYPAD_THREE',
        'KEYPAD_FOUR',
        'KEYPAD_FIVE',
        'KEYPAD_SIX',
        'KEYPAD_SEVEN',
        'KEYPAD_EIGHT',
        'KEYPAD_NINE',
        'KEYPAD_ZERO',
        'KEYPAD_PERIOD',
        'KEYPAD_BACKSLASH',
        'APPLICATION',
        'POWER',
        'KEYPAD_EQUALS',
        'F13',
        'F14',
        'F15',
        'F16',
        'F17',
        'F18',
        'F19',
        'LEFT_CONTROL',
        'CONTROL',
        'LEFT_SHIFT',
        'SHIFT',
        'LEFT_ALT',
        'ALT',
        'OPTION',
        'LEFT_GUI',
        'GUI',
        'WINDOWS',
        'COMMAND',
        'RIGHT_CONTROL',
        'RIGHT_SHIFT',
        'RIGHT_ALT',
        'RIGHT_GUI',
        'modifier_bit'
        ]
}

        # Mouse.LEFT_BUTTON, Mouse.MIDDLE_BUTTON, Mouse.RIGHT_BUTTON
"""
