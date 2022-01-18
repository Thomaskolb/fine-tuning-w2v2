# Thomas Kolb s1027332
# This program parses ASR files (.hyp files) to something more useful

import json

def read(path):
    with open(path, 'r') as asrfile:
        wordsequence = []
        lines = asrfile.read().split('\n')
        for line in lines:
            if(len(line) > 0):
                sequence = json.loads(line)[0]['wordsequence']
                wordsequence += [WordTime(el['wordID'], el['beginTime']) for el in sequence]
        return wordsequence

# Returns sequence of words within wordsequence in between start_time and end_time
def search_sequence(wordsequence, start_time, end_time):
    index = binary_search_closest(wordsequence, start_time)
    sequence = []
    while index < len(wordsequence) and wordsequence[index].start_time < end_time:
        sequence.append(wordsequence[index].word)
        index += 1
    return sequence

# Returns the index of the element with the closest time to start_time
def binary_search_closest(wordsequence, start_time):
    lo, hi = 0, len(wordsequence) - 1
    best_ind = lo
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if wordsequence[mid].start_time < start_time:
            lo = mid + 1
        elif wordsequence[mid].start_time > start_time:
            hi = mid - 1
        else:
            best_ind = mid
            break
        # check if data[mid] is closer to val than data[best_ind] 
        if abs(wordsequence[mid].start_time - start_time) < abs(wordsequence[best_ind].start_time - start_time):
            best_ind = mid
    return best_ind

# 2 tuple consisting of word and starttime
class WordTime:
    def __init__(self, word, start_time):
        self.word = word
        self.start_time = start_time

    def __str__(self):
        return "(" + f"{self.word}, {self.start_time}" + ")"

    def __repr__(self):
        return self.__str__()