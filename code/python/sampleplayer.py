# Thomas Kolb s1027332
# This program takes a list of subtitle sound 3-tuples, displays the subtitle and word error rate and plays the sound

import pygame
import random
import time
import json
import sys

# Function that plays a random sound and displays some info
def play_sound_and_display_info(path):
    with open(path, 'r') as tuplesfile:
        lines = tuplesfile.read().split('\n')
        index = random.randint(0, len(lines))
        info = json.loads(lines[index])
        print('"' + info['text'] + '"\t' + str(info['wer']))
        pygame.mixer.init()
        pygame.mixer.music.load(info['path'])
        pygame.mixer.music.play()
        time.sleep(pygame.mixer.Sound(info['path']).get_length())

if len(sys.argv) < 2:
    print("Please enter the path of the listed data.")
else:
    play_sound_and_display_info(sys.argv[1])