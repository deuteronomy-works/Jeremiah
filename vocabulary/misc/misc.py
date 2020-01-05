# -*- coding: utf-8 -*-
import re

def add_splitter(splits, splitter):

    """
    Adds a spliter back to the splits
    eg: if splitted on space ' '
    ['this', 'is', 'me']
    becomes
    ['this', ' ', 'is', ' ', 'me']
    """

    restruct = []
    no = -1
    for x in splits:
        no += 1
        if no == len(splits) - 1:
            restruct.append(x)
            break
        restruct.append(x)
        restruct.append(splitter)

    return restruct


def escape_unicode(line):
    unicode = {'&nbsp;': '_space__uni_code'}
    
    for code in unicode:
        line = line.replace(code, unicode[code])

    return line


def escape_user_strings(line):
    found = re.findall(r'".*?.*?"', line)
    sngl = []
    if found:
        no = -1
        for f in found:
            no += 1
            sngl.append(f)
            line = line.replace(f, 'sngl____'+str(no))

    found = re.findall(r"'.*?.*?'", line)
    dobl = []
    if found:
        no = -1
        for f in found:
            no += 1
            dobl.append(f)
            line = line.replace(f, 'dobl____'+str(no))

    return sngl, dobl, line


def put_back_unicode(line):
    words = {'_space__uni_code': '&nbsp;'}
    
    for word in words:
        line = line.replace(word, words[word])

    return line


def put_back_user_strings(sngl, dobl, line):
    # single
    no = -1
    for f in sngl:
        no += 1
        line = line.replace('sngl____'+str(no),
                            "<span style='color: #46c28e'>"+sngl[no]+"</span>")

    # double
    no = -1
    for f in dobl:
        no += 1
        line = line.replace('dobl____'+str(no),
                            "<span style='color: #46c28e'>"+dobl[no]+"</span>")

    return line


def fix_span_stat(old_stat):
    # fix escape for less and greater than symbols
    new_stat = old_stat.replace('[[span]]', '<span>').replace('[[jeridespan]]', '</span>')
    return new_stat
