__author__ = 'mjacoby'

import TimeUtilities

class ChapterTimes(object):
    module_name = ''
    chapter_list = []
    def __init__(self):
        self.module_name = ''
        self.chapter_list = []

    def get_total_length(self):
        chapter_durations_list = []
        for chapter in self.chapter_list:
            chapter_durations_list.append(chapter.duration)
        total_seconds_str = TimeUtilities.add_by_timecode_str(chapter_durations_list)
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