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
from layers import get_action
from mappings import do_key_action
from mappings import current_layer_name

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(90)

# Set initial values
encoder_position = 0
encoder_mode = {
    "volume": ["vol_up", "vol_dn"],
    "layer": ["l_up", "l_dn"],
    "mouse": ["m_up", "m_dn"],
}
encoder_mode_names = list(encoder_mode.keys())


def init():
    print("\n\n\n\nBooting\n")
    macropad.pixels[6] = (0, 10, 50)
    macropad.pixels[9] = (0, 10, 50)
    macropad.pixels[11] = (0, 10, 50)
    do_key_action("Mouse")
    print("LAYER:", current_layer_name())
    print("init complete")


# Main Loop
init()
while True:
    key_event = macropad.keys.events.get()
    if key_event:
        try:
            print("LAYER:", current_layer_name())

            if key_event.released:
                key_num = key_event.key_number
                action = get_action(key_num, current_layer_name())
                print("KEY:", key_num, "up")
                print("ACTION:", action)
                do_key_action(action, 1)

            if key_event.pressed:
                key_num = key_event.key_number
                action = get_action(key_num, current_layer_name())
                print("KEY:", key_num, "dn")
                print("ACTION:", action)
                do_key_action(action, 0)

        except Exception as err:
            print("Error: {}, {}".format(err, type(err)))

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
