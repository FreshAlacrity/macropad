# Version 0.1

"""
Based on: MacroPad HID keyboard and mouse demo,
    2021 Unlicense, by Kattni Rembor for Adafruit Industries

The demo sends "a" when the first key is pressed, a "B" when
the second key is pressed, "Hello, World!"
when the third key is pressed, and decreases the volume
when the fourth key is pressed.
It sends a right mouse click when the rotary encoder switch is
pressed. Finally, it moves the mouse left and right when the rotary encoder is rotated
counterclockwise and clockwise respectively.
"""
from adafruit_macropad import MacroPad
# import time

macropad = MacroPad(90)

# set an initial value for the rotary encoder
last_position = 0

# Volume Actions
def increase_volume():
    macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_INCREMENT)

def decrease_volume():
    macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_DECREMENT)

# Mouse Actions
def mouse_r_click():
    macropad.mouse.click(macropad.Mouse.RIGHT_BUTTON)


key_actions = {
    "vol_up": increase_volume,
    "vol_dn": decrease_volume,
    "r_click": mouse_r_click
}

while True:
    key_event = macropad.keys.events.get()

    if key_event:
        if key_event.pressed:
            k = key_event.key_number
            if k == 0:
                macropad.keyboard.send(macropad.Keycode.A)
            if k == 1:
                macropad.keyboard.press(macropad.Keycode.SHIFT, macropad.Keycode.B)
                macropad.keyboard.release_all()
            if k == 2:
                key_actions["vol_dn"]()
                # macropad.keyboard_layout.write("Hello, World!")
            if k == 3:
                key_actions["vol_up"]()

    macropad.encoder_switch_debounced.update()

    if macropad.encoder_switch_debounced.pressed:
        macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_INCREMENT)

    current_position = macropad.encoder

    if macropad.encoder > last_position:
        key_actions["vol_up"]()
        # macropad.mouse.move(x=+5)
        last_position = current_position

    if macropad.encoder < last_position:
        key_actions["vol_dn"]()
        # macropad.mouse.move(x=-5)
        last_position = current_position
