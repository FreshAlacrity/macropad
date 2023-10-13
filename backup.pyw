"""Update CircuitPython and GitHub repo with most recent changes
and open the GitHub Desktop application for quick commits."""

from dirsync import sync
from AppOpener import open as open_application

# Sync everything in the scripts directory
options = {"ctime": True, "twoway": True}
sync("F:/scripts/", "./scripts/", "sync", **options)

# Add option to specify only syncing the README and main.py files
options["only"] = [r".*(README.md)|(main.py)"]
sync("F:/", ".", "sync", **options)
open_application("github desktop")