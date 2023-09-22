# Version 0.1

# CTRL + C > any key to enter REPL, CTRL + D to exit
"""
    = To Do =
[x] get the screen rotated 90 degrees
[ ] click rotary to change between volume control and layer select
[ ] implement improved mousekeys
[ ] add a layer system with layer select via rotary knob
[ ] work on incorporating a pomodoro timer using the time lib
    [ ] show timer progress on the OLED
[ ] count keypresses
[ ] use an array of keynames to map to key numbers
[ ] find the repo for the little ASCII python pet
    [ ] see if we can render the cute faces to the OLED
[ ] attach a second OLED (chained with other STEMMA QT boards?)

Based on: MacroPad HID keyboard and mouse demo,
    Unlicense 2021 by Kattni Rembor for Adafruit Industries
"""

from adafruit_macropad import MacroPad

# import time

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(90)

# Set initial values
last_position = 0
current_layer = 0
mouse_speed = 5
encoder_mode = {
    "volume": ["vol_up", "vol_dn"],
    "layer": ["layer_up", "layer_down"]
}
layers = {
    "Mouse": ["vol_up", "vol_dn"],
    "Cassette Beasts": [
        ["move_up", "w"],
        ["move_down", "s"],
        ["move_right", "d"],
        ["move_left", "a"],
        ["close", "tab", "esc"],
        ["jump", "space"],
        ["sprint", "shift"],
        ["climb", "ctrl"],
        ["map", "m"],
        ["party", "p"],
        ["inventory", "i"],
        ["confirm", "space", "e", "enter"],
        ["menu", "tab", "enter", "esc"],
        ["ui_1", "r"],
        ["magn", "r"],
        ["ui_2", "f"],
        ["sprint", "tab"],
        ["continue", "e"],
        ["page_up", "pg_up"],
        ["page_down", "pg_dn"],
    ],
}
layer_names = list(layers.keys())


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
    macropad.mouse.move(y=+mouse_speed)


def mouse_down():
    macropad.mouse.move(y=-mouse_speed)


def mouse_left():
    macropad.mouse.move(x=-mouse_speed)


def mouse_right():
    macropad.mouse.move(x=+mouse_speed)


# Layer Actions
def layer_up():
    current_layer += 1

def layer_down():
    current_layer -= 1

# @todo add arrow key support
key_actions = {
    "blank": nothing,
    "vol_up": increase_volume,
    "vol_dn": decrease_volume,
    "r_click": mouse_r_click,
    "m_up": mouse_up,
    "m_right": mouse_right,
    "m_left": mouse_left,
    "m_down": mouse_down,
}


def init():
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

            k = key_event.key_number
            layer_name = layer_names[current_layer]
            layout = layers[layer_name]

            action = "blank"
            if k <= len(layout):
                print(type(layout[k]))
                if type(layout[k]) == str:
                    action = layout[k]
                else:
                    action = layout[k][1]
            print("LAYER:", layer_name)
            print("KEY:", k)
            print("ACTION:", action)

    macropad.encoder_switch_debounced.update()

    if macropad.encoder_switch_debounced.pressed:

        macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_INCREMENT)

    current_position = macropad.encoder

    if macropad.encoder > last_position:
        key_actions["vol_up"]()
        last_position = current_position

    if macropad.encoder < last_position:
        key_actions["vol_dn"]()
        # macropad.mouse.move(x=-5)
        last_position = current_position
