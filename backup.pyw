"""Script to copy project scripts from CircuitPython drive to GitHub repository
and open the GitHub Desktop application for quick commits."""

import shutil
from AppOpener import open as open_application

files = ["main", "layers", "layermap", "mappings", "timer"]

for index, name in enumerate(files):
    source = f"F:/{name}.py"
    destination = f"./scripts/{name}.py"
    shutil.copyfile(source, destination)

open_application("github desktop")
