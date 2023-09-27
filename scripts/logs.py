# Since imports that work great in execution aren't being recognized:
# pyright: reportMissingImports=false
# pylint: disable=import-error

import adafruit_logging as logging

# Setup for logging
serial_log = logging.getLogger('test')
LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LOG_LEVEL = LEVELS[0]
serial_log.setLevel(getattr(logging, LEVELS[0]))
serial_log.info(f"\n\nLog level: {LOG_LEVEL}")
# log.error('Error message')

def log(string):
    # Messages at any level less than the one set in the Logger will be ignored
    print("\n")
    serial_log.info(f"\n\n{string}\n")