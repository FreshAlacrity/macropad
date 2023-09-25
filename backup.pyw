import shutil
from AppOpener import open

files = ["main", "layers", "layermap", "mappings", "timer"]

for index, name in enumerate(files):
  source = "F:/{}.py".format(name)
  destination = "./scripts/{}.py".format(name)
  shutil.copyfile(source, destination)
  
open("github desktop")