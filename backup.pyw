import shutil
from AppOpener import open

files = ["main", "layers", "mappings"]

for name in files:
  shutil.copyfile(
    "F:/{}.py".format(name), 
    "./scripts/{}.py".format(name)
    )
  
open("github desktop")