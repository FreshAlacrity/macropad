
def get_layers():
    """Layer Structure/Key Location Keywords:
    "New Layer": {
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
        "Test": {
            "actions": {
                "outer_1": "one",
                "mid_1": "two",
                "inner_1": "three",
                "outer_2": "four",
                "mid_2": "five",
                "inner_2": "six",
                "inner_3": "backspace",
                "thumb": "space",
            }
        },
        "Arrows": {
            "actions": {
                "left_2": "l_click",
                "right_2": "r_click",
                "up": "hold_up_arrow",
                "down": "hold_down_arrow",
                "left": "hold_left_arrow",
                "right": "hold_right_arrow",
                "extra_1": "Mouse",
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
                "extra_1": "Arrows",
                # "down_2": "m_drag", # @todo get this working as a toggle
                # "left_3": "tab_left",
                # "right_3": "tab_right",
            }
        },
        "Game": {
            "actions": {
                # "turn_up": "inherit", # @todo get these working
                # "turn_up": "inherit",
                # "turn_down": "inherit",
                "up": "hold_w",
                "left_2": "q",
                "right_2": "e",
                "down": "hold_s",
                "left": "hold_a",
                "right": "hold_d",
                "extra_1": "m",
                "extra_2": "hold_ctrl",
                "thumb": "hold_shift",
            }
        },
        "Layer Select": {
            "actions": {"turn_up": "ls_up", "turn_down": "ls_dn", "turn_click": "ls_go"}
        },
    }
