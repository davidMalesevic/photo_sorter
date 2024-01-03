#!/usr/bin/env python3

import os
import shutil
import datetime

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the source directory where files are located
src_dir = script_dir

# Set the target directory where files will be moved to (directory containing '_import')
dst_dir = os.path.dirname(script_dir)

# Get a list of all files in the source directory
files = os.listdir(src_dir)

# Loop over the files
for file in files:
    if file.startswith('.') or file.endswith('.py'):
        continue  # Skip hidden files and script files

    # Get the creation time of the file
    ctime = os.stat(os.path.join(src_dir, file)).st_birthtime
    cdate = datetime.datetime.fromtimestamp(ctime)

    # Extract the year, month, and day from the creation time
    year = str(cdate.year)
    month = str(cdate.month)
    day = str(cdate.day)

    # Create the target directory for the year (sibling of '_import')
    target_year_dir = os.path.join(dst_dir, year)
    if not os.path.exists(target_year_dir):
        os.makedirs(target_year_dir)

    # Create the target directory for the specific date within the year
    target_dir = os.path.join(target_year_dir, month, day)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        os.makedirs(os.path.join(target_dir, 'raw'))
        os.makedirs(os.path.join(target_dir, 'jpg'))
        os.makedirs(os.path.join(target_dir, 'export'))

    # Check if the file already exists in the target directory
    basename, ext = os.path.splitext(file)
    target_raw_file = os.path.join(target_dir, 'raw', file)
    target_jpg_file = os.path.join(target_dir, 'jpg', file)

    counter = 1
    while os.path.exists(target_raw_file) or os.path.exists(target_jpg_file):
        # File with the same name already exists, rename the file with an incrementing number
        new_name = f"{basename}_{counter}{ext}"
        target_raw_file = os.path.join(target_dir, 'raw', new_name)
        target_jpg_file = os.path.join(target_dir, 'jpg', new_name)
        counter += 1

    # Move the file to the appropriate folder
    if file.lower().endswith(('.jpg', '.jpeg')):
        shutil.move(os.path.join(src_dir, file), target_jpg_file)
    else:
        shutil.move(os.path.join(src_dir, file), target_raw_file)
