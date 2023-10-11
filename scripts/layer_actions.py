from logger import log
from layer_map import get_layer_map

SETTINGS = {
    "current_layer": 0,
    "selected_layer": 0,
    "layer_names": list(get_layer_map().keys())
}

def num_layers():
    return len(SETTINGS["layer_names"])

# Layer Actions
def current_layer_name():
    return SETTINGS["layer_names"][SETTINGS["current_layer"]]

# @todo test this, it's probably broken
def layer_select(go=True, move=0):
    if go and move == 0:
        set_layer(SETTINGS["layer_names"][SETTINGS["selected_layer"]])
    elif go:
        current = SETTINGS["current_layer"]
        SETTINGS["current_layer"] = (current + move) % num_layers()
        set_layer(current_layer_name())
    else:
        SETTINGS["selected_layer"] = (SETTINGS["selected_layer"] + move) % len(
            SETTINGS["layer_names"]
        )
        print("\n\nTap for\n{}\n".format(SETTINGS["layer_names"][SETTINGS["selected_layer"]]))


def set_layer(layer_name): # , inputs=0, time=sleep_time, entering=True):
    # @todo implement N inputs to leave the layer
    # @todo implement sleep/time to exit layer by timeout
    # @todo implement exit layer to parent
    if layer_name in SETTINGS["layer_names"]:
        SETTINGS["current_layer"] = SETTINGS["layer_names"].index(layer_name)
        SETTINGS["selected_layer"] = SETTINGS["current_layer"]
        log("Current Layer:", current_layer_name())
        return True
    else:
        return False
    
