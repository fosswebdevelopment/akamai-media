__author__ = 'mjacoby'

# This is a simplified FOSS Video Folio JSON creator that assumes the input CSV is conformed
# to have three bitrates only and in the order 1600k, 800k, and 300k.

import csv

with open('jsoninputcsv/json_bitrates_streaming.csv', 'rU') as f: # was 'outputxml/testoutput.csv'
    reader = csv.reader(f)
    csvlist = list(reader)
    print "Starting with list of length:", len(csvlist)-1 # minus one to account for header row
    error_count = 0
    for i in range(1,len(csvlist)): # start at 1 because of header row
        fn_json = "jsonoutput_simple/VideoSourcesFromCSV_" + csvlist[i][0].split("/1600k")[0] + ".json"
        with open(fn_json, 'w') as jfile:
            str_json = "["
            bitrate_label_list = ["1600 kbps", "800 kbps", "300 kbps" ]

            for col in range(len(csvlist[i])):
                #print "column", col, "of", len(csvlist[i])
                str_host = "http://science.video.schoolspecialty.com/"
                #str_filename = csvlist[i][col]
                str_akamai_path = csvlist[i][col] # TODO build this automatically from underscore replacement, or change CSV to reflect Akamai path changes.
                #print str_smh_path, str_filename
                #str_filepath = ""
                str_bitrate = bitrate_label_list[col]

                if len(str_akamai_path) > 0:
                    #print str_host
                    #print str_akamai_path
                    #print str_filename
                    #print str_filename[0:str_filename.index("_h264")]
                    #print str_filename[str_filename.index("_h264")+1:]
                    #str_filepath += str_host + str_filename
                    #print str_filepath, str_bitrate
                    #str_json += '\n\t{\n\t\t"file": "' + str_filepath + '",\n\t\t"label": "' + bitrate_label_list[::-1][col-1] + '"\n\t}'
                    str_json += '\n\t{\n\t\t"file": "' + str_host + str_akamai_path + '",\n\t\t"label": "' + str_bitrate + '"\n\t}'
                    #if str_bitrate != "1600 kbps" and str_bitrate != "1500 kbps" and str_bitrate != "128 kbps": # this is not a good way to do this
                    if col != len(csvlist[i])-1:
                        str_json += ','
            str_json += "\n]"
            #print str_json
            jfile.write(str_json)