# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, no-value-for-parameter, import-error

from logger import log
from layer_actions import set_layer
from layer_actions import layer_select
from mouse_actions import mouse_action
from time_test import time_test


custom_key_actions = {
    "blank": {
        "action": (print, "Key Unassigned"), 
        "hint": "This key left intentionally blank"},
    "ls_up": {
        "action": (layer_select, (False, 1)), 
        "hint": "Scroll up one layout layer"},
    "ls_dn": {
        "action": (layer_select, (False, -1)), 
        "hint": "Scroll down one layout layer"},
    "l_up": {
        "action": (layer_select, (True, 1)), 
        "hint": "Go up one layout layer (immediately)"},
    "l_dn": {
        "action": (layer_select, (True, -1)), 
        "hint": "Go down one layout layer (immediately)"},
    "ls_go": {
        "action": (layer_select, (True, 0)), 
        "hint": "Move to the selected layout layer"}
}

@time_test("Custom action")
def custom_action(action_name, action_type):
    if mouse_action(action_name, action_type):
        # Valid mouse action, mouse action taken, no need to continue
        return True
    elif action_type == "pressed" and set_layer(action_name):
        # Valid layer name, layer now set, no need to continue
        return True
    else:
        if action_name in custom_key_actions:
            action = custom_key_actions[action_name]
            if callable(action):
                # print("Executing basic function")
                action()
            elif len(action) > 1:
                arg = action[1]
                if isinstance(arg, dict):
                    # print("Executing function with named arguments")
                    action[0](**arg)
                if isinstance(arg, tuple):
                    # print("Executing function with tuple arguments")
                    action[0](*arg)
                else:
                    # print("Executing function with other/string arguments")
                    action[0](arg)
            else:
                raise KeyError(f"Custom named action not found: {action_name}  - {action_type}")
        else:
            log(f"Custom action not found: {action_name}  - {action_type}")
