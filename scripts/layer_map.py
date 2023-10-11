# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, pointless-string-statement, missing-function-docstring, no-value-for-parameter


from time_test import time_test
from layers import get_layers

SETTINGS = {}


def get_key_layout(wide=True, left_handed=True):
    def make_tuples(list_in):
        return list(map(lambda n: (n,), list_in))

    # Directional block (never reflected)
    nav_block = [
        "left_2 up right_2".split(),
        "left down right".split(),
        "left_3 down_2 right_3".split(),
    ]

    # Reflected to fit handedness
    main_block = [
        "outer_1 mid_1 inner_1".split(),
        "outer_2 mid_2 inner_2".split(),
        "outer_3 mid_3 inner_3".split(),
    ]

    # From top to bottom or mirrored l/r, depending on orientation:
    extras = "extra_1 extra_2 thumb".split()

    # Initialize the temporary variable
    names = []

    # Assemble a keymap according to macropad rotation + reflection (@todo)
    if not left_handed:
        print("@todo REFLECTION NOT YET IMPLEMENTED")

    if not wide:
        for row in range(3):
            for col in range(3):
                names.append((nav_block[row][col], main_block[row][col]))
        names += make_tuples(extras)
    else:
        for row in range(3):
            for col in range(3):
                names.append((nav_block[row][col], main_block[row][col]))
            names.append((extras[row],))

    return names


def get_layer_map():
    return SETTINGS["LAYER_MAP"]


@time_test("Layer action")
def layer_action(key_ref, layer_name):
    """Finds the names of any actions assigned to this numbered or nicknamed key location"""
    layer_actions = SETTINGS["LAYER_MAP"][layer_name]["actions"]
    
    # Retrieve any names for this key if needed
    if isinstance(key_ref, int):
        key_names = SETTINGS["KEY_LAYOUT"][key_ref]
    else:
        key_names = (key_ref,)
        
    current_layer_actions = [layer_actions[x] for x in key_names if x in layer_actions]
    if current_layer_actions:
        return current_layer_actions
    else:
        # Reimplement falling back to lower layers @later
        layer_actions = SETTINGS["LAYER_MAP"]["Default"]["actions"]
        return [layer_actions[x] for x in key_names if x in layer_actions]


def init():
    SETTINGS["KEY_LAYOUT"] = get_key_layout()
    SETTINGS["LAYER_MAP"] = get_layers()


init()
