def identify(action_name):
    ALIASES = {
        # MACROS:
        "DRIVE_F": "WIN + E > CTRL > CTRL > CTRL + L > write_F: > ENTER",
        # MOUSE
        "R_CLICK": "RIGHT_BUTTON",
        "L_CLICK": "LEFT_BUTTON",
        "M_CLICK": "MIDDLE_BUTTON",
        "RT_CLICK": "RIGHT_BUTTON",
        "LF_CLICK": "LEFT_BUTTON",
        "MD_CLICK": "MIDDLE_BUTTON",
        "RIGHT_CLICK": "RIGHT_BUTTON",
        "LEFT_CLICK": "LEFT_BUTTON",
        "MIDDLE_CLICK": "MIDDLE_BUTTON",
        # "KEYCODE": {
        "WIN": "WINDOWS",
        "CTRL": "CONTROL",
        "PG_DN": "PAGE_DOWN",
        "PG_UP": "PAGE_UP",
        "L_TAB": "LEFT_TAB",
        "L_SHIFT": "LEFT_SHIFT",
        # "CONSUMER_CONTROL": {
        "VOL_DOWN": "VOLUME_DECREMENT",
        "VOLUME_DOWN": "VOLUME_DECREMENT",
        "VOL_DN": "VOLUME_DECREMENT",
        "VOL_UP": "VOLUME_INCREMENT",
        "VOLUME_UP": "VOLUME_INCREMENT",
        "FORWARD": "FAST_FORWARD",
        "FWD": "FAST_FORWARD",
        "NEXT": "SCAN_NEXT_TRACK",
        "PREV": "SCAN_PREVIOUS_TRACK",
        "PAUSE": "PLAY_PAUSE",
        "PLAY": "PLAY_PAUSE",
        "SCREEN_UP": "BRIGHTNESS_INCREMENT",
        "SCREEN_DN": "BRIGHTNESS_INCREMENT",
        "SCREEN_DOWN": "BRIGHTNESS_INCREMENT",
        "BRIGHTER": "BRIGHTNESS_INCREMENT",
        "DIMMER": "BRIGHTNESS_INCREMENT",
        "LT_UP": "BRIGHTNESS_DECREMENT",
        "LT_DN": "BRIGHTNESS_DECREMENT",
        }

    # If the dictionary has it, return the de-aliased version
    # Otherwise just return the input value
    return ALIASES.get(action_name.upper(), action_name)