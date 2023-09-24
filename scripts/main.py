# Version 0.3

# Mu: CTRL + C > any key to enter REPL, CTRL + D to exit

# Based on: MacroPad HID keyboard and mouse demo,
# Unlicense 2021 by Kattni Rembor for Adafruit Induencoder_positiones

import time
from adafruit_macropad import MacroPad
from layers import get_action
from layers import get_layer_color
from layers import get_layer_pattern
from mappings import do_key_action
from mappings import current_layer_name
from mappings import close_out

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(90)

# Settings
init_action = "Mouse"
sleep_at = 100000

# Initial values
idle_time = 0
encoder_position = 0
keys_held = []


def input_action(key_num, index=0):
    action = get_action(key_num, current_layer_name())
    # print("KEY:", key_num, ["down", "up", "hold"][index])
    # print("ACTION:", action)
    do_key_action(action, index)
    # @todo log the action somehow


def sleep():
    print("\n\n\n\n\n\n...zZzzZZ\n")
    for i in range(12):
        macropad.pixels[i] = (0, 0, 0)


def unsleep():
    # @todo light up the keypad corresponding to the *selected_layer*
    global idle_time
    idle_time = 0


def update():
    close_out()
    color = get_layer_color(current_layer_name())
    pattern = get_layer_pattern(current_layer_name())
    for i in pattern:
        macropad.pixels[i] = color


def init():
    print("\n\n\n\n\nBooting...\n")
    do_key_action(init_action)
    update()
    # print("LAYER:", current_layer_name())


# Main Loop
init()
while True:
    idle_time += 1
    try:
        while macropad.keys.events:
            key_event = macropad.keys.events.get()
            if key_event:

                # Adds 3 to skip the rotary encoder inputs
                key_num = key_event.key_number + 3

                if key_event.pressed:
                    input_action(key_num, 0)
                    keys_held.append(key_num)

                if key_event.released:
                    input_action(key_num, 1)
                    keys_held.remove(key_num)

            unsleep()

        if macropad.keys.events.overflowed:
            raise Exception("Key event overflow!")
        # else:
        #    print(keys_held)

        if len(keys_held) == 0:
            if idle_time == sleep_at:
                sleep()

        else:
            for key in keys_held:
                input_action(key, 2)
            unsleep()

        # Check for rotary encoder input
        macropad.encoder_switch_debounced.update()
        current_position = macropad.encoder

        if macropad.encoder_switch_debounced.pressed:
            input_action(2, 0)
            unsleep()

        # Clockwise turn detected
        if macropad.encoder > encoder_position:
            input_action(1, 0)
            unsleep()

        # Counterclockwise turn detected
        elif macropad.encoder < encoder_position:
            input_action(0, 0)
            unsleep()

        encoder_position = current_position

        # Close out any pending actions (mouse movement etc)
        if idle_time == 0:
            update()

    except Exception as err:
        print("Error: {}, {}".format(err, type(err)))
        raise
