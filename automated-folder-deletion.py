#!/usr/bin/python
"""
Automated Folder Archival

This script removes 14 day old build result folders from your desired directory (defaulted to Downloads)
It has been given executable permission to allow you the ease of simply running the script.

Normal operation will delete old build results located at os.path.expanduser(~Downloads)

A custom path can also be used when calling the script using:
-c  --custom path  "custom path entered by user to clean 14 day old folders"

Ex:
./automated-folder-deletion.py
./automated-folder-deletion.py -c "Downloads"
"""

import os
import re
import sys
import time
import shutil
import logging
import argparse

days_to_deletion = 14
default_path = os.path.expanduser("~Downloads")
results_path = "Downloads/automated-folder-deletion.log"

# List that contains a particular keyword within the target directory that indicates specific folders desired to keep
keywords = ['Resume']

def automate_deletion(number_of_days, path):
    """ 
    This function deletes any folder in the home directory's Downloads that is older than the specified number of days. 

    Args:
        number_of_days: The number of days desired to wait before deleting the folders.
        path: The path to the root directory housing the folders
    """
    time_in_secs = time.time() - number_of_days * 86400
    # Loops through the folder paths within the root directory
    for directory in [x[0] for x in os.walk(path)]:
        # Ignores the root folder and allows access to subfolder names as group(2)
        folder = re.match(r'^(.+)/([^/]+)$', directory)
        if folder and os.path.join(folder.group(1),'') == path and not any(key in folder.group(2) for key in keywords):
            if os.path.getmtime(directory) < time_in_secs:
                try:
                    shutil.rmtree(directory)
                    logging.info("Deleted: {}".format(directory))
                except OSError as e:
                    logging.error("{}: unable to delete {}".format(e,directory))
                    continue

if __name__ == "__main__":
    logging.basicConfig(level = 20, filename = results_path, filemode = "a+", format = "%(asctime)-15s %(levelname)-8s %(message)s")
    parser = argparse.ArgumentParser(description = "Cleans up the desired directory of all folders that exceed {} days of age".format(days_to_deletion))
    parser.add_argument('-c', dest = 'custom', help = "Target directory to remove old folders", default=default_path)
    args = parser.parse_args()
    automate_deletion(days_to_deletion, os.path.join(args.custom,''))
