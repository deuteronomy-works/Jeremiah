# -*- coding: utf-8 -*-

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


def fix_span_stat(old_stat):
    # fix escape for less and greater than symbols
    new_stat = old_stat.replace('[[span]]', '<span>').replace('[[;span]]', '</span>')
    return new_stat
