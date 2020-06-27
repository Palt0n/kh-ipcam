"""
source env/Scripts/activate
"""
import os
import re
import argparse
from functools import partial

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("path_dir")
args = vars(ap.parse_args())

path_dir = args["path_dir"] #"photos\person"
list_filepaths = []
list_cam_string = []

prepend = partial(os.path.join, path_dir)
size_total = sum([(os.path.getsize(f) if os.path.isfile(f) else getFolderSize(f)) for f in map(prepend, os.listdir(path_dir))])

count_total = 0
count_delete = 0
for filename in os.listdir(path_dir):
    count_total += 1
    filepath = os.path.join(path_dir, filename)
    match = re.match(r"(\d+\.\d+\.\d+\.\d+_\d+_\d+)", filename)
    if match is None:
        print("IGNORE: {}".format(filepath))
        continue
    cam_string = match.group(0)
    if cam_string in list_cam_string:
        os.remove(filepath)
        count_delete += 1
        print("DELETE: {}".format(filepath))
    else:
        list_cam_string.append(cam_string)

prepend = partial(os.path.join, path_dir)
size_delete = sum([(os.path.getsize(f) if os.path.isfile(f) else getFolderSize(f)) for f in map(prepend, os.listdir(path_dir))])

def human(size):
    B = "B"
    KB = "KB" 
    MB = "MB"
    GB = "GB"
    TB = "TB"
    UNITS = [B, KB, MB, GB, TB]
    HUMANFMT = "%f %s"
    HUMANRADIX = 1024.

    for u in UNITS[:-1]:
        if size < HUMANRADIX : return HUMANFMT % (size, u)
        size /= HUMANRADIX

    return HUMANFMT % (size,  UNITS[-1])

print("{}/{} deleted".format(count_delete, count_total))
print("{} of {} deleted".format(human(size_total - size_delete), human(size_total)))
