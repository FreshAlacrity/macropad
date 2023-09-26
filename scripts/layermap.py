def layer_map():
    return {
        # Note: The first two entries are rotary encoder up/down
        "Default": {
            "pattern": (2, 5, 7),
            "actions": [
                ["vol_up"],
                ["vol_dn"],
                ["Layer Select"],
                ["drive_f"],
                ["lf_click"],
                ["m_up"],
                ["rt_click"],
                ["vol_dn"],
                ["m_lf"],
                ["m_dn"],
                ["m_rt"],
                ["m_stop"],
                ["l_tab"],
                ["m_drag"],
                ["r_tab"],
            ],
        },
        "Mouse": {
            "pattern": (2, 5, 7),
            "actions": [
                [],
                [],
                [],
                [],
                ["lf_click"],
                ["m_up"],
                ["rt_click"],
                [],
                ["m_lf"],
                ["m_dn"],
                ["m_rt"],
                ["m_stop"],
                ["l_tab"],
                ["m_drag"],
                ["r_tab"],
            ],
        },
        "Game": {
            "pattern": (2, 5, 7),
            "actions": [
                [], [], [],
                ["Mouse"], ["quests", "q"], ["move_up", "m_w"], ["inventory", "e"],
                ["crouch", "ctrl"], ["move_left", "m_a"], ["move_down", "m_s"], ["move_right", "m_d"],
                ["sprint", "shift"], ["crouch", "ctrl"], [], ["map", "m"],
            ],
        },
        "Minecraft": {
            "parent": "Game",
            "pattern": (2, 5, 7),
            "color": (50, 0, 0),
            "actions": [
                ["vol_up"],
                ["vol_dn"],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ],
        },
        "Cassette Beasts": {
            "pattern": (2, 5, 7),
            "parent": "Game",
            "actions": [
                ["page_up", "page_up"],
                ["page_down", "page_down"],
                [],
                ["menu", "tab", "enter", "esc"], ["party", "p"], ["move_up", "m_w"], ["inventory", "i"],
                ["climb", "control"], ["move_left", "m_a"], ["move_down", "m_s"], ["move_right", "m_d"],
                ["sprint", "m_shift"], ["jump/confirm", "m_space"], ["continue", "e"], ["map", "m"],
                # try quick tap to sprint to access secondary layer
                # included in the menu: party, map, quests etc
                ["close", "tab", "esc"],
                ["confirm", "space", "e", "enter"],
                ["ui_1", "r"],
                ["magn", "r"],
                ["ui_2", "f"],
            ],
        },
        "Layer Select": {
            "actions": [
                ["ls_dn"],
                ["ls_up"],
                ["ls_go"],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ],
        }
    }
