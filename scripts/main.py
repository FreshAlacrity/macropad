# Version 0.2

# CTRL + C > any key to enter REPL, CTRL + D to exit
"""
    = To Do =
[x] get the screen rotated 90 degrees
[ ] see if the macropad can pretend to be more than one HID
[ ] click rotary to change between volume control and layer select
[ ] implement improved mousekeys
[ ] add a layer system with layer select via rotary knob
[ ] work on incorporating a pomodoro timer using the time lib
    [ ] show timer progress on the OLED
[ ] count keypresses
[ ] add key action for changing the audio in/out
    with the FxSound key combinations
[ ] use an array of keynames to map to key numbers
[ ] find the repo for the little ASCII python pet
    [ ] see if we can render the cute faces to the OLED
[ ] attach a second OLED (chained with other STEMMA QT boards?)

Based on: MacroPad HID keyboard and mouse demo,
    Unlicense 2021 by Kattni Rembor for Adafruit Induencoder_positiones
"""

from adafruit_macropad import MacroPad

# import time

# @todo polish this up better
from layers import list_layer_names
from layers import get_action
layer_names = list_layer_names()

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(90)

# Set initial values
encoder_position = 0
current_layer = 1
mouse_speed = 5
encoder_mode = {
    "volume": ["vol_up", "vol_dn"],
    "layer": ["l_up", "l_dn"],
    "mouse": ["m_up", "m_dn"],
}
encoder_mode_names = list(encoder_mode.keys())


def nothing():
    print("no action")


# Examples
def key_combination():
    macropad.keyboard.press(macropad.Keycode.SHIFT, macropad.Keycode.B)
    macropad.keyboard.release_all()


# Volume Actions
def increase_volume():
    macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_INCREMENT)


def decrease_volume():
    macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_DECREMENT)


# Mouse Setup
def mouse_r_click():
    macropad.mouse.click(macropad.Mouse.RIGHT_BUTTON)


def mouse_up():
    macropad.mouse.move(y=-mouse_speed)


def mouse_down():
    macropad.mouse.move(y=+mouse_speed)


def mouse_left():
    macropad.mouse.move(x=-mouse_speed)


def mouse_right():
    macropad.mouse.move(x=+mouse_speed)


# Layer Actions
def layer_up():
    global current_layer
    current_layer = current_layer + 1


def layer_down():
    global current_layer
    current_layer = current_layer - 1


# @todo add arrow key support
key_actions = {
    "blank": (print, "unassigned"),
    "vol_up": (increase_volume),
    "vol_dn": (decrease_volume),
    "r_click": (mouse_r_click),
    "m_up": (macropad.mouse.move, {"y": -mouse_speed}),
    "m_right": (mouse_right),
    "m_left": (mouse_left),
    "m_dn": (mouse_down),
    "l_up": (layer_up),
    "l_dn": (layer_down),
}

def do_key_action(action_name):
    print("Key action:", action_name)
    if not isinstance(action_name, str):
        action_name = "error"
        # @todo learn to handle errors properly
        print("Action name is not a string!")
    if action_name in key_actions:
        action = key_actions[action_name]
    else:
        action = (print, action_name)

    if type(action) == type(init):
        #  print("Executing function")
        action()
    elif len(action) > 1:
        arg = action[1]
        if isinstance(arg, str):
            #  print("Executing function w/encoder_position argument")
            action[0](arg)
        else:
            #  print("Executing function w/named arguments")
            action[0](**arg)
    else:
        print("Error - key input not a function")

def init():
    print("\n\n\n\nBooting\n")
    print("init complete")


# Main Loop
init()
while True:
    key_event = macropad.keys.events.get()

    if key_event:
        if key_event.pressed:

            # Wrap the layer number to make sure it's valid
            if current_layer >= len(layer_names):
                current_layer = 0
            elif current_layer < 0:
                current_layer = len(layer_names) - 1

            key_num = key_event.key_number
            layer_name = layer_names[current_layer]
            action = get_action(key_num, layer_name)

            print("LAYER:", layer_name)
            print("KEY:", key_num)
            print("ACTION:", action)

            do_key_action(action)

    # Check for rotary encoder input
    macropad.encoder_switch_debounced.update()
    current_position = macropad.encoder

    if macropad.encoder_switch_debounced.pressed:
        macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_INCREMENT)

    # Clockwise turn detected
    if macropad.encoder > encoder_position:
        do_key_action("m_up")
        encoder_position = current_position

    # Counterclockwise turn detected
    elif macropad.encoder < encoder_position:
        do_key_action("m_dn")
        encoder_position = current_position
