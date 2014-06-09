__author__ = 'mjacoby'

def seconds_from_string(time_str):
    # pretty rigid: expects 00:00:00.00... (hh:mm:ss.dddd) time format
    time_list = time_str.split(":")
    total_seconds = int(time_list[0])*3600 + int(time_list[1])*60 + float(time_list[2])
    return total_seconds

def string_from_seconds(seconds_float): # TODO: make this work for decimal (float) seconds
    remaining_seconds_int = int(str(seconds_float).split(".")[0])
    remaining_seconds_decimal_str = str(seconds_float).split(".")[1]
    hours_str = "00"
    if remaining_seconds_int >= 3600:
        hours = remaining_seconds_int/3600
        hours_str = str(hours)
        if len(hours_str) < 2:
            hours_str = "0" + hours_str
        remaining_seconds_int = remaining_seconds_int%3600
    minutes_str = "00"
    if remaining_seconds_int >= 60:
        minutes = remaining_seconds_int/60
        minutes_str = str(minutes)
        if len(minutes_str) < 2:
            minutes_str = "0" + minutes_str
        remaining_seconds_int = remaining_seconds_int%60
    remaining_seconds_str = str(remaining_seconds_int)
    if len(remaining_seconds_str) < 2:
        remaining_seconds_str = "0" + remaining_seconds_str
    total_time_str = hours_str + ":" + minutes_str + ":" + remaining_seconds_str + "." + remaining_seconds_decimal_str
    return total_time_str

def add_by_timecode_str(tc_list):
    sec_total = 0.0
    for tc in tc_list:
        sec_total += seconds_from_string(tc)
    return string_from_seconds(sec_total)

### TESTS ###

#print add_by_timecode_str(["00:01:23", "00:11:01.33"])

#print seconds_from_string("00:01:23.4567")