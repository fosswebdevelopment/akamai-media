__author__ = 'mjacoby'

'''
This will take a legacy FOSSweb audio story playlist (XML) and convert it to
the new format neccessary for the SSI WDF Akamai system.
'''

from lxml import etree
import os
import get_dur_ffprobe
import TimeUtilities
from audio_story_encode import do_encode
from audio_story_encode import do_concatenation_encode
from audio_story_encode import get_path_output

class ChapterTimes(object):
    module_name = ''
    chapter_list = []
    def __init__(self):
        self.module_name = ''
        self.chapter_list = []

    def get_total_length(self):
        total_seconds = 0
        for chapter in self.chapter_list:
            # TODO: switch this to add_by_timecode_str()
            total_seconds += TimeUtilities.seconds_from_string(chapter.duration)
        total_seconds_str = TimeUtilities.string_from_seconds(total_seconds)
        return total_seconds_str

    def add_chapter(self, chapter, verbose=False):
        self.chapter_list.append(chapter)
        if verbose:
            print "Added chapter with title:", chapter.title

class Chapter(object):
    duration = ''
    begin = ''
    title = ''
    def __init__(self):
        self.duration = ''
        self.begin = ''
        self.title = ''

def get_chaptertimes_xml_tree(template_file, chaptertimes_obj):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(template_file, parser)
    #doc = tree.getroot() # not used
    nsmap = {'ssivid': 'http://namespaces.schoolspecialty.com/com.schoolspecialty.wdf.video'}

    # modify total length and module name
    ct = tree.xpath("/ssivid:chapterTimes", namespaces=nsmap)
    ct[0].set('totalLength', chaptertimes_obj.get_total_length())
    #print ct[0].get('totalLength')
    ct[0].set('module', chaptertimes_obj.module_name)
    #print ct[0].get('module')

    # add chapters
    first = ct[0].find("ssivid:chapter", namespaces=nsmap)
    #print first.get("title")
    ct[0].remove(first)
    for chapter in chaptertimes_obj.chapter_list:
        chapter_element = etree.Element("chapter")
        chapter_element.set("begin", chapter.begin)
        chapter_element.set("duration", chapter.duration)
        chapter_element.set("title", chapter.title)
        #print "Adding:", chapter_element
        ct[0].append(chapter_element)
    #print etree.tostring(tree, pretty_print=True)

    return tree

# Traverse module folders, grab playlist file and access source mp3s, transform playlist
def process_audio_stories(path_root, no_encodes=False):
    root_dir_list = [x for x in os.listdir(path_root) if not '.' in x] # exclude elements which have a period (such as .DS_Store and regular files such as .csv)
    #print root_dir_list
    file_mismatches = ''
    json_builder_csv_text = 'Filename (128k)\n'
    for module_dir in root_dir_list:
        this_chaptertimes = ChapterTimes()
        this_chaptertimes.module_name = module_dir
        #print this_chaptertimes.module_name
        audio_stories_path = path_root + '/' + module_dir + '/audio_stories'
        audio_stories_dir = os.listdir(audio_stories_path)
        #print audio_stories_dir
        concat_file_text = '# this is the ffmpeg concat file for ' + module_dir + "\n"
        with open(audio_stories_path + '/playlist.xspf.xml') as playlist:
            print "Attempting to parse: " + audio_stories_path + '/playlist.xspf.xml'
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(playlist, parser)
            nsmap = {'xspf': 'http://xspf.org/ns/0/'}
            dict_tracks = {}
            list_tracks = []
            track_elements = tree.xpath("/xspf:playlist/xspf:tracklist/xspf:track", namespaces=nsmap)
            for track in track_elements: # this could be dict/list comprehensions
                # dictionary mapping
                dict_tracks[track.find("xspf:location", namespaces=nsmap).text] = track.find("xspf:annotation", namespaces=nsmap).text
                list_tracks.append(track.find("xspf:location", namespaces=nsmap).text)
            #print "Dict:", dict_tracks

            mp3_files = sorted([f for f in audio_stories_dir if f.endswith('.mp3')])
            #print mp3_files
            print list_tracks
            log_durations = 'PRE re-encode duration\tPOST re-encode duration\n'
            for track_name in list_tracks:
            # iterate over all the 'location' attributes found in playlist xml
                if track_name in mp3_files:
                # filter out anything not found in the directory list (and log what's missing in the else)
                    this_chapter = Chapter()
                    mp3_file_path = audio_stories_path + '/' + track_name
                    this_chapter.duration = get_dur_ffprobe.clean_ffprobe_output(
                        get_dur_ffprobe.get_duration(mp3_file_path), 0)
                    if not no_encodes:
                        log_durations += this_chapter.duration + "\t" # adding to logfile
                    if not no_encodes:
                        do_encode(mp3_file_path)
                    mp3_file_path_reencoded = get_path_output(mp3_file_path)
                    concat_file_text += "file \'" + mp3_file_path_reencoded + "\'\n"
                    if not no_encodes:
                        log_durations += get_dur_ffprobe.clean_ffprobe_output(
                            get_dur_ffprobe.get_duration(mp3_file_path_reencoded)) + "\n" # adding to logfile
                    this_chapter.begin = this_chaptertimes.get_total_length()
                    this_chapter.title = dict_tracks[track_name]
                    this_chaptertimes.add_chapter(this_chapter, True)
                    print "Chapter begin:\t\t", this_chapter.begin
                    print "Chapter duration:\t", this_chapter.duration + "\n"
                else:
                # this should be only the full-length mp3s which appear in the playlist
                # but have been manually removed from the directories
                    file_mismatches += audio_stories_path + "\t" + track_name + "\n"

        concat_file_path = audio_stories_path + '/ffmpeg_concat_list_' + module_dir + '.txt'
        full_mp3_path = audio_stories_path + '/audio_story_' + module_dir + '.mp3'
        with open(concat_file_path, 'wb') as concat_file:
            concat_file.write(concat_file_text)
        if not no_encodes:
            do_concatenation_encode(concat_file_path, full_mp3_path)

        print "ChapterTimes total length:", this_chaptertimes.get_total_length() + "\n"
        get_chaptertimes_xml_tree('chaptertimes_template.xml', this_chaptertimes).write(audio_stories_path + '/chaptertimes_FOSS_' + module_dir + '.xml', encoding='UTF-8', xml_declaration=True, pretty_print=True)
        path_logfile = audio_stories_path + "/logfile_" + module_dir + ".csv"
        with open(path_logfile, "wb") as logfile:
            logfile.write(log_durations)
        json_builder_csv_text += 'audio_story_' + module_dir + '.mp3\n'
    json_builder_csv_file_path = path_root + '/json_builder_' + path_root.split("/")[-1] + '.csv'
    with open(json_builder_csv_file_path, 'wb') as json_builder_csv_file:
        json_builder_csv_file.write(json_builder_csv_text)
    print file_mismatches


#process_audio_stories('/Users/mjacoby/Desktop/audio_stories_test', True)
