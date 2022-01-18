# Thomas Kolb s1027332
# This program parses vtt files to something more useful

import re

# Function that reads vtt file and returns a list of Caption objects
def read(path):
    with open(path, 'r') as vttfile:
        lines = vttfile.read().split('\n')
        times = [(l[:12], l[-12:]) for l in lines[2::3]]
        texts = lines[3::3]
        return [Caption(texts[i], times[i][0], times[i][1]) for i in range(min(len(times), len(texts)))]

# Turns subtitle time format into seconds using a regex
def get_time_in_seconds(time):
    hours, minutes, seconds = re.match('([0-9]{2})\:([0-9]{2})\:([0-9]{2}\.[0-9]{3})$', time).groups()
    return 3600*int(hours) + 60*int(minutes) + float(seconds)

# Caption object: text, start time, end time
class Caption:
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.text}, {self.start} -> {self.end}"

    def __repr__(self):
        return self.text
