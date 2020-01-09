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

def escape_html_metachars(word):
    html_metachars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}
    for entity in html_metachars:
        word = word.replace(entity, html_metachars[entity])
    return word


def escape_unicode(line):
    unicode = {'&nbsp;': 'jeride__space__uni_code'}
    
    for code in unicode:
        line = line.replace(code, unicode[code])

    return line


def escape_user_comments(line):
    found = re.findall(r'#.*.*.*\r\n?', line)
    print('f: ', found)
    sngl = []
    if found:
        no = -1
        for f in found:
            no += 1
            jeride_no = 'jeride__sngl_com____'+str(no)
            line = line.replace(f, jeride_no)
            f = f.replace('\r\n', '\u2029')
            sngl.append(f)
            
            print('esc no: ', no, jeride_no, sngl[no])

    # replace double quote first
    line = line.replace('"""', 'jeride_comm__ent')
    found = re.findall(r'jeride_comm__ent\r\n*.*.*.*\r\n*jeride_comm__ent', line)
    dobl = []
    if found:
        no = -1
        for f in found:
            no += 1
            jeride_no = 'jeride__dobl_com____'+str(no)
            line = line.replace(f, jeride_no)
            f = f.replace('\r\n', '\u2029')
            dobl.append(f)
            print('double esc no: ', no, jeride_no, dobl[no])

    return sngl, dobl, line


def escape_user_strings(line):
    found = re.findall(r'".*?.*?.*?"', line)
    sngl = []
    if found:
        no = -1
        for f in found:
            no += 1
            sngl.append(f)
            line = line.replace(f, 'jeride__sngl____'+str(no))

    found = re.findall(r"'.*?.*?.*?'", line)
    dobl = []
    if found:
        no = -1
        for f in found:
            no += 1
            dobl.append(f)
            line = line.replace(f, 'jeride__dobl____'+str(no))

    return sngl, dobl, line


def put_back_unicode(line):
    words = {'jeride__space__uni_code': '&nbsp;'}
    
    for word in words:
        line = line.replace(word, words[word])

    return line


def put_back_user_comments(sngl, dobl, line):
    # single
    no = -1
    for f in sngl:
        no += 1
        esc_sngl = f
        print('f: ', f)
        span_stat = "<span style='color: #D79FB3'>"+esc_sngl+"</span>"
        print('span stat: ', span_stat)
        jeride_no = 'jeride__sngl_com____'+ str(no)
        line = line.replace(jeride_no, span_stat)
        print('no: ', no, jeride_no, sngl[no])

    # double
    no = -1
    for f in dobl:
        no += 1
        esc_dobl = f
        print('f: ', f)
        span_stat = "<span style='color: #D79FB3'>"+esc_dobl+"</span>"
        print('span stat: ', span_stat)
        jeride_no = 'jeride__dobl_com____' + str(no)
        line = line.replace(jeride_no, span_stat)
        print('double no: ', no, jeride_no, dobl[no])

    # put back escaped triple quotes
    line = line.replace('jeride_comm__ent', '"""')

    return line


def put_back_user_strings(sngl, dobl, line):
    # single
    no = -1
    for f in sngl:
        no += 1
        # escape html chars
        esc_sngl = escape_html_metachars(sngl[no])
        line = line.replace('sngl____'+str(no),
                            "<span style='color: #46c28e'>"+esc_sngl+"</span>")

    # double
    no = -1
    for f in dobl:
        no += 1
        esc_dobl = escape_html_metachars(dobl[no])
        line = line.replace('dobl____'+str(no),
                            "<span style='color: #46c28e'>"+esc_dobl+"</span>")

    return line


def fix_span_stat(old_stat):
    # fix escape for less and greater than symbols
    new_stat = old_stat.replace('[[span]]', '<span>').replace('[[jeridespan]]', '</span>')
    return new_stat
