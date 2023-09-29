# boot.py runs only after a hard reset - push the button to load it!
# WARNING: Make sure your changes are completely written out before you reset, to avoid confusion and filesystem corruption.

# To get the drive back if this works: just use the reset button
# To send the drive into write mode once, edit or delete the toggle file
# To get the drive back if this fails, use Safe Mode: the status LED will blink briefly a few times after you press RESET and if you press RESET during the blinks, the board will enter safe mode (then once the drive is back, comment out the code here and RESET again to run the usual code)

# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

import storage
from logger import log

MESSAGE = "NEXT BOOT: BE A USB"
FILE_PATH = "toggle.txt"

def can_write_itself():
    """Sets up the macropad so it can write to itself"""
    try:
        # Set the drive as writable and disconnect the USB connection
        storage.disable_usb_drive()
        storage.remount("/", readonly=False)
        
        # Attempt to write the next-boot-usb message to the file
        with open(FILE_PATH, mode="w", encoding="utf-8") as f:
            f.write(MESSAGE)
            f.close()
    except OSError as _:
        # Currently read-only, so do nothing
        pass


def check_file():
    try:
        """Boots the keyboard with the drive visible unless the toggle file has been edited or deleted"""
        # Check the file for the message that says to show itself as a USB drive
        with open(FILE_PATH, mode="r", encoding="utf-8") as f:
            test = f.read()
            f.close()
            if not test == MESSAGE:
                can_write_itself()
            else:
                log("Booting in USB drive mode")
    except OSError as _:
        # Couldn't open the file, so boot writable and make one
        can_write_itself()
        
check_file()