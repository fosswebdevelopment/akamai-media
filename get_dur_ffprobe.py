__author__ = 'mjacoby'
# base from http://stackoverflow.com/users/6946/anurag-uniyal
# in http://stackoverflow.com/questions/9896644/getting-ffprobe-information-with-python

import os, sys, subprocess, shlex, re, csv
from subprocess import call

def get_duration(filename, decimal_seconds_min_digits=0, verbose=False):
    cmnd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if verbose:
        print "Attempting to ffprobe file:", filename
    out, err =  p.communicate()
    #print "==========output=========="
    #print out
    for item in out.split("\n"):
        if "duration" in item:
            return item.strip()
    if err:
        print "========= error ========"
        print err
        return "ERROR"

def clean_ffprobe_output(dur_string, decimal_seconds_min_digits=0):
    dur = dur_string.split("=")[1]
    dur_hours_str = dur.split(":")[0]
    if len(dur_hours_str) == 1:
        dur_hours_str = "0" + dur.split(":")[0]
    dur_minutes_str = dur.split(":")[1]
    if decimal_seconds_min_digits > 0:
        dur_seconds_raw = float(dur.split(":")[2])
        decimal_seconds_raw = str(dur_seconds_raw).split(".")[1]
        if len(str(decimal_seconds_raw)) > decimal_seconds_min_digits:
            decimal_seconds_raw = decimal_seconds_raw[0:decimal_seconds_min_digits]
        dur_seconds_clean = str(dur_seconds_raw).split(".")[0] + "." + decimal_seconds_raw
    else: # just using zero if zero or negative
        dur_seconds_clean = int(round(float(dur.split(":")[2])))
    dur_seconds_clean_padded = str(dur_seconds_clean)
    if len(dur_seconds_clean_padded.split(".")[0]) == 1:
        dur_seconds_clean_padded = "0" + dur_seconds_clean_padded
    #print float(dur_seconds_clean_padded) - float(dur.split(":")[2]) # check deltas
    dur_clean = dur_hours_str + ':' + dur_minutes_str + ':' + dur_seconds_clean_padded
    return dur_clean

### TESTING ###

testing_list = [
    "duration=00:01:23",
    "duration=00:01:23.45",
    "duration=00:01:23.4567",
    "duration=00:01:23.456789"
]

for ffprobe_output in testing_list:
    print "ATTEMPTING TEST:\t\t", ffprobe_output
    print "TEST RESULT:\t\t\t", clean_ffprobe_output(ffprobe_output), "\n"