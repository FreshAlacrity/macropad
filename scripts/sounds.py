from time import monotonic

SETTINGS = {
    "TONES": [196, 220, 246, 262, 294, 330, 349, 392, 440, 494, 523, 587],
    "queue": [],
    "active": False,
    "end_time": 0
    }


def tone(num, duration=0.1):
    if SETTINGS["active"]:
        SETTINGS["queue"].append((num, duration))
    else:
        SETTINGS["end_time"] = monotonic() + duration
        SETTINGS["macropad"].start_tone(SETTINGS["TONES"][num])
        SETTINGS["active"] = True


def sound_init(macropad):
    SETTINGS["macropad"] = macropad

    # Play a little boot-up tune
    for num in range(3,6):
        tone(num)


def key_sound(key_num):
    tone(key_num, 0.04)


def sound_check():
    if SETTINGS["active"] and monotonic() > SETTINGS["end_time"]:
        SETTINGS["macropad"].stop_tone()
        SETTINGS["active"] = False
        if SETTINGS["queue"]:
            tone(*SETTINGS["queue"].pop(0))
