# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, no-value-for-parameter, import-error


from logger import log
from layer_map import get_layer_map
from time_test import time_test


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


def set_layer(layer_name, action_type): # , inputs=0, time=sleep_time, entering=True):
    # @todo implement N inputs to leave the layer
    # @todo implement sleep/time to exit layer by timeout
    # @todo implement exit layer to parent
    if layer_name in SETTINGS["layer_names"]:
        if action_type == "pressed":
            SETTINGS["current_layer"] = SETTINGS["layer_names"].index(layer_name)
            SETTINGS["selected_layer"] = SETTINGS["current_layer"]
            log("Current Layer:", current_layer_name())
            
        # Let the action handler know this action is to set a layer
        return True
    else:
        return False
    

@time_test("Layer action")
def layer_action(action_name, action_type):
    layer_actions = {
        "ls_up": {
            "action": (False, 1), 
            "hint": "Scroll up one layout layer"},
        "ls_dn": {
            "action": (False, -1), 
            "hint": "Scroll down one layout layer"},
        "l_up": {
            "action": (True, 1), 
            "hint": "Go up one layout layer (immediately)"},
        "l_dn": {
            "action": (True, -1), 
            "hint": "Go down one layout layer (immediately)"},
        "ls_go": {
            "action": (True, 0), 
            "hint": "Move to the selected layout layer"}
    }
    
    if set_layer(action_name, action_type):
        # Valid layer name (layer set if action_type is "pressed")
        return True
    elif action_name in layer_actions:
        layer_select(*layer_actions[action_name]["action"])
        return True
    else:
        return False
