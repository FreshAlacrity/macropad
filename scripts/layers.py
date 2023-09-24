from random import randint
from random import seed

layout = {
    # Note: The first two entries are rotary encoder up/down
    "Default": [
        ["vol_dn"], ["vol_up"], ["Layer Select"],
        ["vol_up"], ["lf_click"], ["m_up"], ["rt_click"],
        ["vol_dn"], ["m_lf"], ["m_dn"], ["m_rt"],
        ["m_stop"], ["l_tab"], ["m_drag"], ["r_tab"],
    ],
    "Mouse": [
        [], [], ["Layer Select"],
        [], ["lf_click"], ["m_up"], ["rt_click"],
        [], ["m_lf"], ["m_dn"], ["m_rt"],
        ["m_stop"], ["l_tab"], ["m_drag"], ["r_tab"],
    ],
    "Game": [
        [], [], [],
        [], [], [], [],
        [], [], ["move_up", "m_w"], ["inventory", "e"],
        [], ["move_left", "m_a"], ["move_down", "m_s"], ["move_right", "m_d"],
    ],
    "Cassette Beasts": [
        [], [], [],
        [], [], [], [],
        [], ["test", "T"], ["move_up", "m_w"], ["inventory", "i"],
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
    "Layer Select": [
        ["ls_dn"], ["ls_up"], ["ls_go"],
        [], [], [], [],
        [], [], [], [],
        [], [], [], [],
    ],
    "New": [
        [], [], [],
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

def get_parent_layer():
    return "Default"  # @todo

def get_layer_pattern():
    return (2, 5, 7) # @todo

def get_layer_color(name):
    seed(sum(map(ord, name)))
    vals = []
    for v in range(3):
        vals.append(randint(0, 255))
    total = sum(vals)

    def reg(num):
        return int(num / (total / 100))
    return tuple(map(reg, vals))

def get_action(key_num, layer_name):

    # Set default action
    action_name = "blank"

    # Limited loop so it can't break if the base layer is blank
    for attempt in range(3):
        if has_action(layer_name, key_num):
            action_name = layout[layer_name][key_num]
            if not isinstance(action_name, str):
                if len(action_name) == 1:
                    action_name = action_name[0]
                else:
                    action_name = action_name[1]
            break
        else:
            layer_name = get_parent_layer()

    return action_name
