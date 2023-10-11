# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error

# Disabled for quick prototyping:
# pylint: disable=broad-exception-raised, no-value-for-parameter

import adafruit_logging as logging
from time import monotonic
from time_test import time_test


LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

SETTINGS = {
        "READ_ONLY": False, 
        "LOGGER": logging.getLogger("macropad"), 
        "LOG_LEVEL": 0
    }


# @todo get this working so it restores the USB connection
@time_test("File write attempt")
def log_to_file(log_text):
    try:
        modes = {
            "Read": "r",  # Errors if it doesn't exist
            "Append": "a",
            "Write": "w",  # Creates if it doesn't exist
            "Create": "x",  # Errors if it *does* exist
        }
        file_path = "/logs/most_recent.txt"
        with open(file_path, mode=modes["Append"], encoding="utf-8") as f:
            f.write(f"\n{monotonic()}: {log_text}")
            f.flush()
    except OSError as _:
        # Typical error when the filesystem isn't writeable
        print("Drive is in USB mode")
        SETTINGS["READ_ONLY"] = True
        # ; reset with the button to change back (or uncomment out the drive-disabling code in boot.py)
        return False


def log(*args):
    log_text = " ".join(map(str, args))

    # Messages at any level less than the one set in the Logger will be ignored
    SETTINGS["LOGGER"].info(f"\n  {log_text}\n")
    if not SETTINGS["READ_ONLY"]:
        log_to_file(log_text)


def init():
    SETTINGS["LOGGER"].setLevel(SETTINGS["LOG_LEVEL"])
    log("Log level:", LEVELS[SETTINGS["LOGGER"].getEffectiveLevel()])


init()
