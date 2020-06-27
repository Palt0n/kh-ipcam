"""
source env/Scripts/activate
"""
import os
import re
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("path_dir")
args = vars(ap.parse_args())

path_dir = args["path_dir"] #"photos\person"
list_filepaths = []
list_cam_string = []
count = 0
count_delete = 0
for filename in os.listdir(path_dir):
    count += 1
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
print("{}/{} deleted".format(count_delete, count))
