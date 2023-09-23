# Version 0.2

# CTRL + C > any key to enter REPL, CTRL + D to exit

# Based on: MacroPad HID keyboard and mouse demo,
# Unlicense 2021 by Kattni Rembor for Adafruit Induencoder_positiones


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

def input_action(key_num, index=0):
    indexTranlation = ["down", "up"]
    # issue here: layer change doesn't seem to be sticking
    action = get_action(key_num, current_layer_name())
    print("LAYER:", current_layer_name())
    # print("KEY:", key_num, indexTranlation[index])
    print("ACTION:", action)
    do_key_action(action, index)
    # @todo log the action somehow

def init():
    print("\n\n\n\nBooting\n")

    # @todo light up the keypad corresponding to the *selected_layer*
    macropad.pixels[6] = (0, 10, 50)
    macropad.pixels[9] = (0, 10, 50)
    macropad.pixels[11] = (0, 10, 50)

    do_key_action("Default")
    print("LAYER:", current_layer_name())
    print("init complete")


# Main Loop
init()
while True:
    key_event = macropad.keys.events.get()
    # @todo can this get more than one event per loop?
    if key_event:
        try:
            print("LAYER:", current_layer_name())

            # Add two to the key number to skip the rotary encoder inputs
            key_num = key_event.key_number + 3

            if key_event.released:
                input_action(key_num, 1)

            if key_event.pressed:
                input_action(key_num, 0)

        except Exception as err:
            print("Error: {}, {}".format(err, type(err)))

    # Check for rotary encoder input
    macropad.encoder_switch_debounced.update()
    current_position = macropad.encoder

    if macropad.encoder_switch_debounced.pressed:
        input_action(2, 0)

    # Clockwise turn detected
    if macropad.encoder > encoder_position:
        input_action(1, 0)

    # Counterclockwise turn detected
    elif macropad.encoder < encoder_position:
        input_action(0, 0)

    encoder_position = current_position
