import os.path
import re
import errno
from itertools import groupby
import collections

def valida_ficheiros(files):
    for f in files:
        if not os.path.isfile(f):
            return False

    return True

# Grouping string by consecutive chars and return number of groups
# Also, has minimum threshold
def count_group_char(s, char, min_chars = -1):
    result = 0
    groups = groupby(s)

    groupByChars = [(label, sum(1 for _ in group)) for label, group in groups]

    for g in groupByChars:
        if g[0] == char and g[1] >= min_chars:
            result += 1

    return result

def validate_sequence(seq):

    result = True

    if not seq:
        result = False
        
    return result

def search_keywords(keywords, text):
    result = []

    res = re.findall(r'[\w\-]+', text)

    for kw in keywords:
        if kw in res:
            result.append(kw)

    return result

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def has_substrings(text, list_str):
    return any(substring in text for substring in list_str)