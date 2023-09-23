layout = {
        "Mouse": ["vol_up", "vol_dn"],
        "Game": [
            [], [], [], [],
            [], [], ["move_up", "m_w"], ["inventory", "e"],
            [], ["move_left", "m_a"], ["move_down", "m_s"], ["move_right", "m_d"],
        ],
        "Cassette Beasts": [
                [], [], [], [],
                [], [], ["move_up", "m_w"], ["inventory", "i"],
                [], ["move_left", "m_a"], ["move_down", "m_s"], ["move_right", "m_d"],
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
        "New": [
            [], [], [], [],
            [], [], [], [],
            [], [], [], [],
        ]
}

def list_layer_names():
    return list(layout.keys())

def has_action(layer_name, key_num):
    if not key_num < len(layout[layer_name]):
        raise Exception("This layer does not have a key number that high")
    return len(layout[layer_name][key_num]) > 0

def get_action(key_num, layer_name):
    # Set default action
    action_name = "blank"

    # @todo here fall through to lower layer

    if has_action(layer_name, key_num):
        action_name = layout[layer_name][key_num]
        if not isinstance(action_name, str):
            if len(action_name) == 1:
                action_name = action_name[0]
            else:
                action_name = action_name[1]

    if not isinstance(action_name, str):
        raise Exception("This action is not a string!")

    return action_name
