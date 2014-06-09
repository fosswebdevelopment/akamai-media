__author__ = 'mjacoby'

# Want to take any reasonably valid timecode string and conform it to hh:MM:ss.dd including leading zeros
# only include dd decimal seconds if they are present in the input, that is, no .00

def timecode_conform(tcIn):
    tcOut = ""

    tcList = tcIn.split(":")

    hours = ""
    minutes = ""
    seconds = ""

    if len(tcList) > 0 and len(tcList) < 4:
        #handle seconds first
        sec_str = tcList[-1]
        if "." in sec_str:
            sec_dec_part = sec_str.split(".")[1]
            sec_int_part = sec_str.split(".")[0]
            if len(sec_int_part) == 1:
                sec_int_part = "0" + sec_int_part
            seconds = sec_int_part + "." + sec_dec_part
        else:
            if len(sec_str) == 1:
                seconds = "0" + sec_str
            else:
                seconds = sec_str
        # now minutes
        if len(tcList) > 1:
            min_str = tcList[-2]
            if len(min_str) == 1:
                minutes = "0" + min_str
            else:
                minutes = min_str
        else:
            minutes = "00"
        # now hours
        if len(tcList) > 2:
            hr_str = tcList[-3]
            if len(hr_str) == 1:
                hours = "0" + hr_str
            else:
                hours = hr_str
        else:
            hours = "00"
        tcOut = hours + ":" + minutes + ":" + seconds
        return tcOut
    else:
        print "Input timecode (" + tcIn + ") was either too short or too long."
        return False

#tests
'''
testList = ["3:12", "2:55.1", "0:01:30.00", "10:30:20", "0:03:12.11"]
for t in testList:
    print "Input:  " + t
    print "Output: " + timecode_conform(t) + "\n"
'''