# Thomas Kolb s1027332
# This program contains functions to parse a caption text to match the appropriate rules for training

from num2words import num2words
from nltk.tokenize import word_tokenize
import re

import nltk
nltk.download('punkt')

interpunction = ['.', '...', '!', '?']
forbidden_formats = ['.{1,}\-.{1,}', '[A-Z]{1,}\:', '[0-9]{1,}\.[0-9]{1,}', '[0-9]{1,}e']

# Configurations
# Currently active configuration
active_config = 2
# Allow for capitalization of first word of sentence in configuration
config_capitalization = [False, False, True, True]
# Allowed characters
config_allowed = []
# Ignore these characters completely by removing them
config_ignore = []
# Convert characters of dict from key to value
config_convert = [] 

# Configuration 1
config_allowed.append(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'
    , 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\''])
config_ignore.append(['.', ',', '!', '?', '-', ':', '%', '&', '`'])
config_convert.append({'é':'e', 'è':'e', 'ë':'e', 'ê':'e', 'ö':'o', 'ó':'o', 'ï':'i', 'ü':'u', })

# Configuration 2
config_allowed.append(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'
    , 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\'', '.', ',', '!', '?', '-', ':'])
config_ignore.append(['%', '&', '`'])
config_convert.append({'é':'e', 'è':'e', 'ë':'e', 'ê':'e', 'ö':'o', 'ó':'o', 'ï':'i', 'ü':'u', })

# Configuration 3
config_allowed.append(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'
    , 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\'', '.', ',', '!', '?', '-', ':', '%', '&', '`'])
config_allowed[2] += map(lambda a: a.upper(), config_allowed[2][:26])
config_ignore.append([])
config_convert.append({'é':'e', 'è':'e', 'ë':'e', 'ê':'e', 'ö':'o', 'ó':'o', 'ï':'i', 'ü':'u', })

# Function that filters out captions that don't match requirements
# If it is acceptable it will return an edited caption text
def acceptable_caption_text(caption_text, join_symbol):
    word_list = word_tokenize(caption_text)
    new_word_list = []
    follow_with_capital = False
    for word in word_list:
        # Filter for all upper letters, star symbol and regex formats
        if ((word.isupper() and len(word) > 1)
                or word == '*' 
                or any([re.match(exp, word) for exp in forbidden_formats])):
            return ''
        word = number_to_words(word)
        # Capitalize word after interpunction (except ',')
        if follow_with_capital:
            word = word.capitalize()
            follow_with_capital = False
        if not config_capitalization[active_config-1]:
            word = word.lower()
        new_word, accepted = config_filter(word)
        if len(new_word) > 0:
            new_word_list.append(new_word)
        elif not accepted:
            return ''
        if word in interpunction and config_capitalization[active_config-1]:
            follow_with_capital = True
    # Capitalize first word
    if config_capitalization[active_config-1]:
        new_word_list[0] = new_word_list[0].capitalize()
    return join_symbol.join(new_word_list)

# Changes a word for different configurations; returns '' when word is not allowed
def config_filter(word):
    new_word = ''
    for c in word:
        if c in config_ignore[active_config-1]:
            continue
        elif c in config_convert[active_config-1]:
            new_word += config_convert[active_config-1].get(c)
        elif c not in config_allowed[active_config-1]:
            return '', False
        else:
            new_word += c
    return new_word, True

# Function that tries to parse string to a number, if that goes turn it into a word
def number_to_words(word):
    try:
        num = int(word)
        word = num2words(num, lang='nl')
    except:
        pass
    return word