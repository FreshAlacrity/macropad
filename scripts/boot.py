# boot.py runs only after a hard reset - push the button to load it!
# WARNING: Make sure your changes are completely written out before you reset, to avoid confusion and filesystem corruption.

# To get the drive back, use Safe Mode: the status LED will blink briefly a few times after you press RESET and if you press RESET during the blinks, the board will enter safe mode (then once the drive is back, comment out the code here and RESET again to run the usual code)

# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error, c-extension-no-member

"""
import storage

# Set the drive as writable and disconnect the USB connection
# Required to write to the drive
storage.disable_usb_drive()
storage.remount("/", readonly=False)
"""
