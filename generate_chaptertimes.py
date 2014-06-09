__author__ = 'mjacoby'

# Generate chaptertimes XML from template and CSV with well-defined columns
# This is an initial simple version that only accommodates one chapter and doesn't do escaping etc

from lxml import etree
from timecodeConform import timecode_conform

import csv

def generateXML(file_template, csv_row, dry_run=False):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_template, parser)
    #doc = tree.getroot() # not used
    nsmap = {'ssivid': 'http://namespaces.schoolspecialty.com/com.schoolspecialty.wdf.video'}

    output_filename = csv_row[0]
    module_name = csv_row[1]
    total_length = "0" + csv_row[2]
    begin_time = "0" + csv_row[3]
    title_text = csv_row[4]

    print output_filename, module_name, total_length, begin_time, title_text

    # get the chapterTimes section
    # modify totalLength attribute and module attribute
    ct = tree.xpath("/ssivid:chapterTimes", namespaces=nsmap)
    ct[0].set('totalLength', total_length)
    #print ct[0].get('totalLength')
    ct[0].set('module', module_name)
    #print ct[0].get('module')

    # get the chapter item
    # modify the bgin time and the title
    ch = tree.xpath("ssivid:chapter", namespaces=nsmap)
    #print ch
    ch[0].set('begin', begin_time)
    #print ch[0].get('begin')
    ch[0].set('title', title_text)
    #print ch[0].get('title')

    if not dry_run:
        tree.write("chaptertimes_new/" + output_filename, encoding='UTF-8', xml_declaration=True, pretty_print=True)


with open('input_chaptertimes/SecondRoundAdditions_tpv.csv', 'rU') as csv_input:
    csv_reader = csv.reader(csv_input)
    csv_list = list(csv_reader)
    for i in range(1, len(csv_list)):
        #print csv_list[i]
        generateXML("chaptertimes_template.xml", csv_list[i])