from random import randint
from random import seed

layout = {
    # Note: The first two entries are rotary encoder up/down
    "Default": {
        "pattern": (2, 5, 7),
        "actions": [
            ["vol_dn"],
            ["vol_up"],
            ["Layer Select"],
            ["vol_up"],
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
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            ["move_up", "m_w"],
            ["inventory", "e"],
            [],
            ["move_left", "m_a"],
            ["move_down", "m_s"],
            ["move_right", "m_d"],
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
            ["inventory", "e"],
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
# @todo update this when auto-constructing layers:
layers_count = len(layout)


def list_layer_names():
    return list(layout.keys())


def has_action(actions_list, key_num):
    if not key_num < len(actions_list):
        raise Exception("This layer does not have a key number that high")

    return len(actions_list[key_num]) > 0


def get_parent_layer(layer_name):
    if hasattr(layout[layer_name], "parent"):
        print(layer_name, "has parent")
        return layout[layer_name]["parent"]
    else:
        print(layer_name, "has NO parent")
        return "Default"


def map_to_pattern(layer_name, start=3):
    has_action = []
    actions = layout[layer_name]["actions"]
    key_indexes = range(12)
    for i in key_indexes:
        if len(actions[i + start]) > 0:
            has_action.append(i)
    return has_action


def get_layer_pattern(layer_name="Default"):
    if "pattern" in layout[layer_name]:
        return layout[layer_name]["pattern"]
    else:
        return map_to_pattern(layer_name)


def get_layer_color(layer_name):
    if "color" in layout[layer_name]:
        return layout[layer_name]["color"]
    else:
        seed(sum(map(ord, layer_name)))

        vals = []
        for v in range(3):
            vals.append(randint(0, 255))
        total = sum(vals)

        def reg(num):
            return int(num / (total / 50))

        return tuple(map(reg, vals))


def get_action(key_num, layer_name):

    # Set default action
    action_name = "blank"

    # Limited loop so it can't break if the base layer is blank
    for attempt in range(layers_count - 1):
        actions_list = layout[layer_name]["actions"]
        if has_action(actions_list, key_num):
            action_name = actions_list[key_num]
            if not isinstance(action_name, str):
                if len(action_name) == 1:
                    action_name = action_name[0]
                else:
                    action_name = action_name[1]
            break
        else:
            layer_name = get_parent_layer(layer_name)

    return action_name
