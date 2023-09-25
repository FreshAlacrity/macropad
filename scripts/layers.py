from random import randint
from random import seed
from layermap import layer_map  # type: ignore

layout = layer_map()
layers_count = len(layout)


def get_layer_names():
    return list(layout.keys())


def has_action(actions_list, key_num):
    """Function checks whether the given key position is assigned an action in the given layer action array."""
    if not key_num < len(actions_list):
        raise LookupError("This layer does not have a key number that high")

    return len(actions_list[key_num]) > 0


def get_parent_layer(layer_name):
    if "parent" in layout[layer_name]:
        return layout[layer_name]["parent"]
    else:
        return "Default"


def map_to_pattern(layer_name, start=3):
    action_indexes = []
    actions = layout[layer_name]["actions"]
    key_indexes = range(12)
    for i in key_indexes:
        if len(actions[i + start]) > 0:
            action_indexes.append(i)
    return action_indexes


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
        for _ in range(3):
            vals.append(randint(0, 255))
        total = sum(vals)

        def reg(num):
            return int(num / (total / 50))

        return tuple(map(reg, vals))


def get_action(key_num, layer_name):

    # Set default action
    action_name = "blank"

    # Limited loop so it can't break if the base layer is blank
    for _ in range(layers_count - 1):
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
