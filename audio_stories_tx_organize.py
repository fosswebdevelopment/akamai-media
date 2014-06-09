__author__ = 'mjacoby'

'''
Traverse the audio_stories_tx directory structure, combining files at the module level. At the same time, probe the
lengths of the component files to generate the info needed for chaptertimes generation. Structure resembles:
audio_stories_tx/
    english/
    spanish/
    test/
        Air, Weather, and Earth/
            01_Matter/
                Page 047.mp3
                Page 048.mp3
                Page 049.mp3
                Page 050.mp3
            02_What Is All around Us_/
            03_Clouds/
            ...
            refs_g2_04_Glossary/
'''

import os
import unicodecsv
import get_dur_ffprobe
import TimeUtilities
import audio_story_encode

PATH_ROOT_TEST = '/Users/mjacoby/Documents/FOSSweb/Audio Stories/audio_stories_tx/test'
SKIP_ENCODES = True

root_dir_list = sorted([d for d in os.listdir(PATH_ROOT_TEST) if not os.path.isfile(PATH_ROOT_TEST + "/" + d)])
print "Root directory listing:", root_dir_list

for module_directory in root_dir_list:

    module_directory_full_path = PATH_ROOT_TEST + "/" + module_directory
    module_name_alnum_tx = ''.join(ch for ch in module_directory if ch.isalnum()) + "TX"

    chapter_list = sorted([d for d in os.listdir(module_directory_full_path) if not os.path.isfile(module_directory_full_path + "/" + d)])
    #chapter_list = [f for f in chapter_list if not f[-4] == "."] # this should now be redundant based on use of os.path.isfile() above
    print "Module directory listing:", chapter_list

    # create/init concat list for module
    ffmpeg_concat_list_path = module_directory_full_path + "/ffmpeg_concat_list_" + module_name_alnum_tx + ".txt"
    ffmpeg_concat_list_file = open(ffmpeg_concat_list_path, "wb")
    ffmpeg_concat_list_file.write('# this is the ffmpeg concat file for ' + module_name_alnum_tx + "\n")

    # create chapter list file for module
    chapter_list_file = open(module_directory_full_path + "/chapter_list_" + module_name_alnum_tx + ".tsv", "wb")
    #chapter_list_file_writer = unicodecsv.writer(chapter_list_file, encoding='utf-8')
    #chapter_list_file.write('Chapter Name, Chapter Duration, Chapter Start Time\n')

    module_current_duration_str = "00:00:00"

    for chapter_directory in chapter_list:
        chapter_directory_full_path = module_directory_full_path + "/" + chapter_directory
        mp3_file_list = sorted([mp3 for mp3 in os.listdir(chapter_directory_full_path) if mp3.endswith(".mp3")])
        #print "Chapter directory list for", chapter_directory,"(mp3s only):", mp3_file_list

        # get durations for each chapter
        chapter_duration_str = "00:00:00"
        for mp3_file in mp3_file_list:
            dur = get_dur_ffprobe.clean_ffprobe_output(get_dur_ffprobe.get_duration(chapter_directory_full_path + "/" + mp3_file), 2)
            print "This segment's duration (" + mp3_file + "):", dur
            chapter_duration_str = TimeUtilities.add_by_timecode_str([chapter_duration_str, dur])
            # WRITE each segment to the full module ffmpeg concat list
            ffmpeg_concat_list_file.write("file \'" + chapter_directory_full_path + "/" + mp3_file + "\'\n")
        print "Full chapter duration:", chapter_duration_str, "\n"

        # WRITE to chapter list CSV
        chapter_directory_clean = str(chapter_directory).replace(",", "_")
        chapter_list_file.write(chapter_directory_clean + "\t" + chapter_duration_str + "\t" + module_current_duration_str + "\n")

        # add chapter duration with total duration
        module_current_duration_str = TimeUtilities.add_by_timecode_str([module_current_duration_str, chapter_duration_str])

    print "Module total duration:", module_current_duration_str

    # close files
    ffmpeg_concat_list_file.close()
    chapter_list_file.close()

    if not SKIP_ENCODES:
        mp3_file_full_path = module_directory_full_path + "/audio_story_" + module_name_alnum_tx + ".mp3"
        audio_story_encode.do_concatenation_encode(ffmpeg_concat_list_path, mp3_file_full_path)