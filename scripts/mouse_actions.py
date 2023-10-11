# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, no-value-for-parameter

from usb_hid import devices
from logger import log
from adafruit_hid.mouse import Mouse
from time_test import time_test


SETTINGS = {
    "mouse_speed": 10,
    "mouse_scoot": 2
}
MOUSE_DELTA = {"x": 0, "y": 0}

m = Mouse(devices)

# @todo add support for toggling click-and-drag
# @todo add support for mouse wheel move and click
# Rolls the mouse wheel away from the user one unit:
# m.move(wheel=-1)

@time_test("Mouse move")
def mouse_move(x_delta, y_delta):
    speed = SETTINGS["mouse_speed"]
    log(f"X Delt: {x_delta} Y Delt: {y_delta} Speed: {speed}")
    MOUSE_DELTA["x"] = MOUSE_DELTA["x"] + x_delta * speed
    MOUSE_DELTA["y"] = MOUSE_DELTA["y"] + y_delta * speed

@time_test("Update mouse")
def update_mouse():
    # Called at the end of the main loop
    if MOUSE_DELTA["x"] != 0 or MOUSE_DELTA["y"] != 0:
        m.move(x=MOUSE_DELTA["x"], y=MOUSE_DELTA["y"])
        MOUSE_DELTA["x"] = 0
        MOUSE_DELTA["y"] = 0
    # print("\n----------\n")
    
@time_test("Mouse action")
def mouse_action(action_name, action_type):
    moves = {
        "mouse_right": ((SETTINGS["mouse_scoot"], 0), (1, 0)),
        "mouse_left": ((-SETTINGS["mouse_scoot"], 0), (-1, 0)),
        "mouse_up": ((0, -SETTINGS["mouse_scoot"]), (0, -1)),
        "mouse_down": ((0, SETTINGS["mouse_scoot"]), (0, 1))
    }
    if action_name not in moves:
        return False
    elif action_type == "pressed":
        mouse_move(*moves[action_name][0])
        return True
    elif action_type == "held":
        mouse_move(*moves[action_name][1])
        return True