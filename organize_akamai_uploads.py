__author__ = 'mjacoby'

import os
import shutil
import csv

ROOT_PATH = '/Users/mjacoby/Desktop/audio_stories_tx_upload'
VERBOSE = False

print os.getcwd()
os.chdir(ROOT_PATH)
print os.getcwd()

file_list = os.listdir(ROOT_PATH)
#print file_list

csv_file = open("akamai_upload_items.csv", "wb")
csv_writer = csv.writer(csv_file)
#csv_writer.writerow(["test key", "test value"])

for f in file_list:
    if f.startswith(".") or f.endswith(".csv"):
        print "Excluding", f
    else:
        dir_name = "_".join(f.split("_")[0:-1])
        if VERBOSE:
            print dir_name
        file_name = f.split("_")[-1]
        if VERBOSE:
            print file_name

        source_path = ROOT_PATH + "/" + f
        if VERBOSE:
            print "source_path:", source_path
        dest_path = ROOT_PATH + "/" + dir_name
        if VERBOSE:
            print "dest_path:", dest_path

        try:
            csv_writer.writerow([dir_name + "/" + file_name])
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            shutil.move(source_path, dest_path + "/" + file_name)
        except:
            if VERBOSE:
                print "PROBLEM with moving", source_path
                raise
            else:
                raise
        if VERBOSE:
            print "\n"

csv_file.close()