"""Update CircuitPython and GitHub repo and open
the GitHub Desktop application for quick commits."""

# Later: find and duplicate all .py files in the main directory, not just listed ones

import os
import shutil
from AppOpener import open as open_application

file_names = ["main.py", "layers.py", "layermap.py", "mappings.py", "display.py", "logger.py", "tamtam.py", "text.py", "timetest.py"]

def copy_files(source, destination, names):
    """Copies files from one path location to another"""
    for name in names:
        print(f"Copying from {source}{name} to {destination}{name}")
        shutil.copyfile(f"{source}{name}", f"{destination}{name}")

def sync_file(paths):
    """Copies the most recent file to the other locations specified"""
    edited_date = list(map(os.path.getmtime, paths))
    most_recent = edited_date.index(max(edited_date))
    copy_from = paths[most_recent]
    
    # Filter out copies (files that are already identical to the most recent)
    paths = filter(lambda a : os.path.getmtime(a) != max(edited_date), paths)
    
    # Update the files
    for path in paths:
        print(f"Copying from {copy_from} to {path}")
        shutil.copyfile(copy_from, path)

copy_files("F:/", "./scripts/", file_names)
sync_file(["F:/README.md", "./README.md"])
open_application("github desktop")
