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
    """ " Layer Structure/Key Location Keywords:

    New Layer": {
            "actions": {
                "turn_up": "",
                "turn_down": "",
                "turn_click": "",
                "left_2": "",
                "up": "",
                "right_2": "",
                "left": "",
                "down": "",
                "right": "",
                "left_3": "",
                "down_2": "",
                "right_3": "",
                "outer_1": "",
                "mid_1": "",
                "inner_1": "",
                "outer_2": "",
                "mid_2": "",
                "inner_2": "",
                "outer_3": "",
                "mid_3": "",
                "inner_3": "",
                "extra_1": "",
                "extra_2": "",
                "thumb": "",
            }
        }
    """
    return {
        "Default": {
            "actions": {
                "turn_up": "vol_up",
                "turn_down": "vol_dn",
                "turn_click": "Layer Select"
                # @todo add cut copy paste?
            }
        },
        "Mouse": {
            "actions": {
                # "turn_up": "inherit", # @todo get these working
                # "turn_down": "inherit",
                # "turn_click": "uninherit",
                "left_2": "l_click",
                "right_2": "r_click",
                "up": "mouse_up",
                "down": "mouse_down",
                "left": "mouse_left",
                "right": "mouse_right",
                # "down_2": "m_drag", # @todo get this working as a toggle
                "left_3": "l_tab",
                "right_3": "r_tab",
            }
        },
        "Game": {
            "actions": {
                "turn_up": "inherit",
                "turn_down": "inherit",
                "up": "hold_w",
                "left_2": "q",
                "right_2": "e",
                "down": "hold_s",
                "left": "hold_a",
                "right": "hold_d",
                "left_3": "l_tab",
                "right_3": "r_tab",
                "extra_1": "m",
                "extra_2": "hold_ctrl",
                "thumb": "hold_shift",
            }
        },
        "Layer Select": {
            "actions": {
                "turn_up": "ls_up", 
                "turn_down": "ls_dn", 
                "turn_click": "ls_go"
            }
        },
    }
