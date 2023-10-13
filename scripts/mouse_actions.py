# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, no-value-for-parameter, import-error, unused-import

from usb_hid import devices
from logger import log
from adafruit_hid.mouse import Mouse
from time_test import time_test
from aliases import check_prefix


SETTINGS = {
    "mouse_speed": 10,
    "scroll_speed": 0.5,
    "frame": 0,
    "mouse_scoot": 2
}
MOUSE_DELTA = {"x": 0, "y": 0, "wheel": 0}

m = Mouse(devices)

# @todo add support for toggling click-and-drag
# @todo add support for mouse wheel move and click
# Rolls the mouse wheel away from the user one unit:
# m.move(wheel=-1)

@time_test("Mouse move")
def mouse_move(x_delta, y_delta):
    speed = SETTINGS["mouse_speed"]
    # log(f"X Delt: {x_delta} Y Delt: {y_delta} Speed: {speed}")
    MOUSE_DELTA["x"] = MOUSE_DELTA["x"] + x_delta * speed
    MOUSE_DELTA["y"] = MOUSE_DELTA["y"] + y_delta * speed


def mouse_scroll(direction):
    multiply_by = 1
    if "down" in direction:
        multiply_by = -1
    
    distance = max(int(SETTINGS["scroll_speed"]), 1)
    
    MOUSE_DELTA["wheel"] += distance * multiply_by
        

@time_test("Update mouse")
def update_mouse():
    # Called at the end of the main loop
    types = ("x", "y", "wheel")
    if any([MOUSE_DELTA[t] != 0 for t in types]):
        m.move(**MOUSE_DELTA)
        for t in types:
            MOUSE_DELTA[t] = 0
    # print("\n----------\n")


@time_test("Mouse action")
def mouse_action(action_name, action_type):
    moves = {
        "right": (1, 0),
        "left": (-1, 0),
        "up": (0, -1),
        "down": (0, 1)
    }
    
    action_name, move_mouse = check_prefix(action_name, "mouse_")
    action_name, scroll = check_prefix(action_name, "scroll_")
    
    if move_mouse:
        # @later figure out scoots
        scoot = False
        # action_name, scoot = check_prefix("scoot_")
        if scoot and action_type == "pressed":
            # @later multiply by scoot value here
            mouse_move(*moves[action_name])
        elif action_type == "held":
            mouse_move(*moves[action_name])
        return True
    elif scroll:
        mouse_scroll(action_name)
        return True
    else:
        return False