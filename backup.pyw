"""Script to copy project scripts from CircuitPython drive to GitHub repository
and open the GitHub Desktop application for quick commits."""

# Later: also check which version of the readme is most recent and copy to the other location

import os
import shutil
from AppOpener import open as open_application

files = ["main", "layers", "layermap", "mappings", "timer"]

for index, name in enumerate(files):
    source = f"F:/{name}.py"
    destination = f"./scripts/{name}.py"
    shutil.copyfile(source, destination)

def sync_file(paths=["F:/README.md", "./README.md"]):
    edited_date = list(map(os.path.getmtime, paths))
    most_recent = edited_date.index(max(edited_date))
    copy_from = paths[most_recent]
    for path in paths:
        if path != copy_from:
            print(f"Copying from {copy_from} to {path}")
            shutil.copyfile(copy_from, path)

sync_file()

open_application("github desktop")
