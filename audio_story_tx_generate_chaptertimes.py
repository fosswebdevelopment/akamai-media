__author__ = 'mjacoby'
# -*- coding: utf-8 -*-

'''
Generate chaptertimes XML for texas audio stories, based on input CSV which supports special unicode characters
'''

import unicodecsv
from lxml import etree
from fosswebmedia import Chapter, ChapterTimes
import os


#FILENAME_INPUT_TEST = "Texas Audio Story Chapter Names - Reorganized - Air Weather and Earth (Spanish).csv"


def passthrough_csv(file_path_input, file_path_output, verbose=True):
    with open('input_chaptertimes/' + file_path_input, 'rU') as input_chapterlist_file:
        csv_reader = unicodecsv.reader(input_chapterlist_file)
        with open('chaptertimes_new/' + file_path_output, 'wb') as output_chapterlist_file:
            csv_writer = unicodecsv.writer(output_chapterlist_file)
            csv_writer.writerows(csv_reader)


def get_generated_chaptertimes_xml_tree(template_file, chaptertimes_obj, verbose=False):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(template_file, parser)
    #doc = tree.getroot() # not used
    nsmap = {'ssivid': 'http://namespaces.schoolspecialty.com/com.schoolspecialty.wdf.video'}

    # modify total length and module name
    ct = tree.xpath("/ssivid:chapterTimes", namespaces=nsmap)
    ct[0].set('totalLength', chaptertimes_obj.get_total_length())
    if verbose:
        print ct[0].get('totalLength')
    ct[0].set('module', chaptertimes_obj.module_name)
    if verbose:
        print ct[0].get('module')

    # add chapters
    first = ct[0].find("ssivid:chapter", namespaces=nsmap)
    if verbose:
        print first.get("title")
    ct[0].remove(first)
    for chapter in chaptertimes_obj.chapter_list:
        chapter_element = etree.Element("chapter")
        chapter_element.set("begin", chapter.begin)
        chapter_element.set("duration", chapter.duration)
        chapter_element.set("title", chapter.title)
        if verbose:
            print "Adding:", chapter_element
        ct[0].append(chapter_element)
    #print etree.tostring(tree, pretty_print=True)

    return tree

def get_module_name_from_chapterlist_filename(filename):
    module_name = filename.split(".csv")[0].split("Texas Audio Story Chapter Names - Reorganized - ")[1]
    return module_name

def get_chaptertimes_from_chapterlist(chapterlist_file, module_name, verbose=True):
    csv_reader = unicodecsv.reader(chapterlist_file)

    this_chaptertimes = ChapterTimes()

    # generate Chapter items
    for row in csv_reader:
        this_chapter = Chapter()
        this_chapter.title = row[0]
        this_chapter.duration = row[1]
        this_chapter.begin = row[2]
        this_chaptertimes.add_chapter(this_chapter)

    # complete ChapterTimes item (incl module name - from filename?)
    this_chaptertimes.module_name = module_name

    return this_chaptertimes


def process_chapterlist_item(input_chapterlist_file_path):
    input_chapterlist_filename = input_chapterlist_file_path.split("/")[-1]
    with open(input_chapterlist_file_path, 'rU') as input_chapterlist_file:
        this_chaptertimes = get_chaptertimes_from_chapterlist(input_chapterlist_file, get_module_name_from_chapterlist_filename(input_chapterlist_filename))
        get_generated_chaptertimes_xml_tree('chaptertimes_template.xml', this_chaptertimes).write('chaptertimes_new/chaptertimes_FOSS_TX_' + get_module_name_from_chapterlist_filename(input_chapterlist_filename) + '.xml', encoding='UTF-8', xml_declaration=True, pretty_print=True)

PATH_ROOT = "/Users/mjacoby/Documents/python/multistreamparse/input_chapterlists"

#list_dir_root = os.listdir(PATH_ROOT)
list_dir_root = sorted([f for f in os.listdir(PATH_ROOT) if os.path.isfile(PATH_ROOT + "/" + f)])

for f in list_dir_root:
    print "Attempting to process chapter list at:", PATH_ROOT + "/" + f
    process_chapterlist_item(PATH_ROOT + "/" + f)