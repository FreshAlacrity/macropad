# Version 0.2

# CTRL + C > any key to enter REPL, CTRL + D to exit

# Based on: MacroPad HID keyboard and mouse demo,
# Unlicense 2021 by Kattni Rembor for Adafruit Induencoder_positiones

# import time
from adafruit_macropad import MacroPad
from layers import get_action
from mappings import do_key_action
from mappings import current_layer_name
from mappings import close_out

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(90)

# Set initial values
encoder_position = 0
keys_held = []


def input_action(key_num, index=0):
    print("KEY:", key_num, ["down", "up", "hold"][index])

    # issue here: layer change doesn't seem to be sticking
    action = get_action(key_num, current_layer_name())
    print("LAYER:", current_layer_name())
    print("ACTION:", action)
    do_key_action(action, index)
    # @todo log the action somehow


def init():
    print("\n\n\n\nBooting\n")

    # @todo light up the keypad corresponding to the *selected_layer*
    macropad.pixels[6] = (0, 10, 50)
    macropad.pixels[9] = (0, 10, 50)
    macropad.pixels[11] = (0, 10, 50)

    do_key_action("Mouse")
    # print("LAYER:", current_layer_name())
    # print("init complete")


# Main Loop
init()
while True:
    try:
        while macropad.keys.events:
            key_event = macropad.keys.events.get()
            if key_event:
                # @todo can this get more than one event per loop?

                # Add two to the key number to skip the rotary encoder inputs
                key_num = key_event.key_number + 3

                if key_event.pressed:
                    input_action(key_num, 0)
                    keys_held.append(key_num)

                if key_event.released:
                    input_action(key_num, 1)
                    keys_held.remove(key_num)

        if macropad.keys.events.overflowed:
            raise Exception("Key event overflow!")
        # else:
        #    print(keys_held)

        for key in keys_held:
            input_action(key, 2)

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

        # Implement registered mouse movements etc
        close_out()
    except Exception as err:
        print("Error: {}, {}".format(err, type(err)))
        raise
