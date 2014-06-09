__author__ = 'mjacoby'

'''
This script will help encode FOSSweb audio stories, including concatenating multi-file playlists into one long mp3
'''

import subprocess

'''
ROOT_PATH = 'input_audio_stories/'

file_name_input = 'AirAndWeather_ch02.mp3'

file_path_input = ROOT_PATH + file_name_input

file_name_output = file_name_input.split('.mp3')[0] + '_reencode' + '.mp3'

file_path_output = ROOT_PATH + file_name_output

#subprocess.call(['ffmpeg', '-y', '-i', file_path_input, '-acodec', 'libmp3lame', '-ab', '128k', file_path_output])
'''


def get_path_output(file_path_input):
    file_path_output = file_path_input.split('.mp3')[0] + '_reencode' + '.mp3'
    return file_path_output


def do_encode(file_path_input, bitrate="128k"):
    file_path_output = get_path_output(file_path_input)
    subprocess.call(['ffmpeg', '-y', '-i', file_path_input, '-acodec', 'libmp3lame', '-ab', bitrate, file_path_output])


def do_concatenation_encode(ffmpeg_concat_list, file_path_output):
    subprocess.call(['ffmpeg', '-y', '-f', 'concat', '-i', ffmpeg_concat_list, '-c', 'copy', file_path_output])


do_concatenation_encode("/Users/mjacoby/Documents/FOSSweb/Audio Stories/audio_stories_tx/english/Air, Weather, and Earth/ffmpeg_concat_list_AirWeatherandEarthTX.txt", "/Users/mjacoby/Documents/FOSSweb/Audio Stories/audio_stories_tx/english/Air, Weather, and Earth/audio_story_AirWeatherandEarthTX.mp3")