def layer_map():
    return {
        # Note: The first two entries are rotary encoder up/down
        "Default": {
            "pattern": (2, 5, 7),
            "actions": [
                ["vol_dn"],
                ["vol_up"],
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
                ["crouch", "ctrl"],
                ["move_left", "m_a"],
                ["move_down", "m_s"],
                ["move_right", "m_d"],
                ["sprint", "shift"], ["crouch", "ctrl"], [], [],
            ],
        },
        "Minecraft": {
            "parent": "Game",
            "pattern": (2, 5, 7),
            "color": (50, 0, 0),
            "actions": [
                ["vol_dn"],
                ["vol_up"],
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
                [],
                [],
                [],
                [],
                ["test", "T"],
                ["move_up", "m_w"],
                ["inventory", "i"],
                [],
                ["move_left", "m_a"],
                ["move_down", "m_s"],
                ["move_right", "m_d"],
                [],
                [],
                [],
                [],
                ["close", "tab", "esc"],
                ["jump", "space"],
                ["sprint", "shift"],
                ["climb", "ctrl"],
                ["map", "m"],
                ["party", "p"],
                ["confirm", "space", "e", "enter"],
                ["menu", "tab", "enter", "esc"],
                ["ui_1", "r"],
                ["magn", "r"],
                ["ui_2", "f"],
                ["sprint", "tab"],
                ["continue", "e"],
                ["page_up", "pg_up"],
                ["page_down", "pg_dn"],
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
