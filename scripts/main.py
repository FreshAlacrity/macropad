# Version 0.4

# CTRL+ALT+R > CTRL+C to enter REPL, CTRL+D to soft reboot

# Based on: MacroPad HID keyboard and mouse demo,
# Unlicense 2021 by Kattni Rembor for Adafruit Induencoder_positiones

# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised


from adafruit_macropad import MacroPad
from layers import get_action
from layers import get_layer_color
from layers import get_layer_pattern
from mappings import do_key_action
from mappings import current_layer_name
from mappings import close_out
from tamtam import update_display
from tamtam import tam_tam
from logs import log

# Settings
INIT_ACTION = "Cassette Beasts"
SLEEP_AT = 100000
DEBUG = True

log("TEST LOG")

# Initialize and rotate the MacroPad so that the OLED is on the left
macropad = MacroPad(90)


# Initial values
SETTINGS = {
    "idle_time": 0,
    "encoder_position": 0
}
keys_held = []


def input_action(current_key_num, index=0):
    """Retrieves and executes the action assigned to this key number on the current layer."""
    action = get_action(current_key_num, current_layer_name())
    do_key_action(action, index)
    # @todo here - log the action somehow


def get_idle_time():
    return SETTINGS["idle_time"]


def sleep():
    # @todo figure out why I can't import tam_tam
    tam_tam("asleep")
    for i in range(12):
        macropad.pixels[i] = (0, 0, 0)


def unsleep():
    SETTINGS["idle_time"] = 0


def update():
    if SETTINGS["idle_time"] == 0:
        close_out()
        color = get_layer_color(current_layer_name())
        pattern = get_layer_pattern(current_layer_name())
        for i in pattern:
            macropad.pixels[i] = color
    elif get_idle_time() % 100 == 0:
        # Only updates the display every N frames
        update_display()


def init():
    print("\n\n\n\n\nBooting...\n")
    do_key_action(INIT_ACTION)
    update()
    update_display()

    # Loop forever so you can enjoy your image
    #while True:
        #pass

    # print("LAYER:", current_layer_name())


# Main Loop
init()
while True:
    SETTINGS["idle_time"] += 1
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
            if SETTINGS["idle_time"] == SLEEP_AT:
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
        if macropad.encoder > SETTINGS["encoder_position"]:
            input_action(0, 0)
            unsleep()

        # Counterclockwise turn detected
        elif macropad.encoder < SETTINGS["encoder_position"]:
            input_action(1, 0)
            unsleep()

        SETTINGS["encoder_position"] = current_position

        # Close out any pending actions (mouse movement etc)
        update()

    except Exception as err:
        print("Error: {}, {}".format(err, type(err)))
        raise
