layout = {
        "Mouse": ["vol_up", "vol_dn"],
        "Cassette Beasts": [
                ["move_up", "w"],
                ["move_down", "s"],
                ["move_right", "d"],
                ["move_left", "a"],
                ["close", "tab", "esc"],
                ["jump", "space"],
                ["sprint", "shift"],
                ["climb", "ctrl"],
                ["map", "m"],
                ["party", "p"],
                ["inventory", "i"],
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
}

def list_layer_names():
    return list(layout.keys())

def get_action(key_num, layer_name):
    layer_layout = layout[layer_name]

    # Set default action
    action = "blank"
    if key_num <= len(layer_layout):
        if isinstance(layer_layout[key_num], str):
            action = layer_layout[key_num]
        else:
            action = layer_layout[key_num][1]
    return action
