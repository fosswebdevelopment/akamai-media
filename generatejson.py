__author__ = 'mjacoby'

import csv

with open('inputcsv/testoutput_new.csv', 'rU') as f: # was 'outputxml/testoutput.csv'
    reader = csv.reader(f)
    csvlist = list(reader)
    error_count = 0
    for i in range(len(csvlist)):
        fn_json = "outputjson/VideoSourcesFromRTMPMultistream_" + csvlist[i][0] + ".json"
        with open(fn_json, 'w') as j:
            str_json = "["
            brlabellist = ["300 kbps", "800 kbps", "1600 kbps" ] # don't forget to account for 1500k files etc

            for col in range(1,len(csvlist[i])):
                #print "column", col, "of", len(csvlist[i])
                str_host = "http://science.video.schoolspecialty.com/"
                str_akamai_path = csvlist[i][col]
                str_filename = csvlist[i][col].split("/")[-1]
                #print str_smh_path, str_filename
                str_filepath = ""
                str_bitrate = ""

                if len(str_akamai_path) > 0:
                    # determine bitrate
                    if "1600k" in str_akamai_path or "1600K" in str_akamai_path:
                        str_bitrate = "1600 kbps"
                    elif "1500k" in str_akamai_path or "1500K" in str_akamai_path:
                        str_bitrate = "1500 kbps"
                    elif "800k" in str_akamai_path or "800K" in str_akamai_path:
                        str_bitrate = "800 kbps"
                    elif "300k" in str_akamai_path or "300K" in str_akamai_path:
                        str_bitrate = "300 kbps"
                    elif "mp3" in str_akamai_path:
                        str_bitrate = "128 kbps"
                    elif "FOSS_TPV_Prototype_Measurement" in str_akamai_path:
                        str_bitrate = "1600 kbps"
                    else:
                        print "Bitrate could not be determined for file:", str_filename, "Assuming bitrate 300k"
                        str_bitrate = "300 kbps"
                        error_count += 1
                    #print str_bitrate

                if len(str_filename) > 0:
                    #print str_host
                    print str_akamai_path
                    print str_filename
                    #print str_filename[0:str_filename.index("_h264")]
                    #print str_filename[str_filename.index("_h264")+1:]
                    if "_H264" in str_filename:
                        str_filepath += str_host + str_filename[0:str_filename.index("_H264")] + "/" + str_filename[str_filename.index("_H264")+1:]
                    elif "_h264" in str_filename:
                        str_filepath += str_host + str_filename[0:str_filename.index("_h264")] + "/" + str_filename[str_filename.index("_h264")+1:]
                    elif "_1600k" in str_filename:
                        str_filepath += str_host + str_filename[0:str_filename.index("_1600k")] + "/" + str_filename[str_filename.index("_1600k")+1:]
                    elif "_800k" in str_filename:
                        str_filepath += str_host + str_filename[0:str_filename.index("_800k")] + "/" + str_filename[str_filename.index("_800k")+1:]
                    elif "_300k" in str_filename:
                        str_filepath += str_host + str_filename[0:str_filename.index("_300k")] + "/" + str_filename[str_filename.index("_300k")+1:]
                    elif "_1500K" in str_filename:
                        str_filepath += str_host + str_filename[0:str_filename.index("_1500K")] + "/" + str_filename[str_filename.index("_1500K")+1:]
                    elif "_300K" in str_filename:
                        str_filepath += str_host + str_filename[0:str_filename.index("_300K")] + "/" + str_filename[str_filename.index("_300K")+1:]
                    else:
                        str_filepath += str_host + str_filename
                    print str_filepath, str_bitrate
                    #str_json += '\n\t{\n\t\t"file": "' + str_filepath + '",\n\t\t"label": "' + brlabellist[::-1][col-1] + '"\n\t}'
                    str_json += '\n\t{\n\t\t"file": "' + str_host + str_akamai_path + '",\n\t\t"label": "' + str_bitrate + '"\n\t}'
                    #if str_bitrate != "1600 kbps" and str_bitrate != "1500 kbps" and str_bitrate != "128 kbps": # this is not a good way to do this
                    if col != len(csvlist[i])-1:
                        str_json += ','
            str_json += "\n]"
            j.write(str_json)
    print "Bitrate errors:", error_count