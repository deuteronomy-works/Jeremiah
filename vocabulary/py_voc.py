# -*- coding: utf-8 -*-
import re
from vocabulary.py_user_defined import UserDefined
from vocabulary.types.base import base_types, base_types_dict, base_operand,\
base_operand_repl, base_functions,base_func_dict, base_types_repl
from vocabulary.types.user_defined import user_func_dict
from vocabulary.types.referenced import ref_prop_name
from vocabulary.misc.misc import add_splitter, fix_span_stat, escape_unicode,\
put_back_unicode, escape_user_strings, put_back_user_strings, escape_user_comments
from vocabulary.misc.misc_py import SplitParenthesis

class Pyvoc():


    def __init__(self, conts):
        self.content = conts
        self.base_types = base_types_repl
        self.base_types_dict = base_types_repl
        self.operand_types = ['+', '-', '=', '/', '*']
        self.escape_parentesis = ['[', ']', '{', '}', '(', ')']
        self.space_char = " "
        self.replace_processes = ['spaceless', 'base']
        self.lines = []
        self.r_lines_len = 0
        self.curr_type = None
        self.curr_class = None
        self.curr_func = None
        self.curr_par_indent = 0
        self.curr_type_name = ''
        self.curr_index = 0
        self.variables = {}

    def start(self):

        # Find user defined
        user_def = UserDefined(self.content)
        self.content = user_def.start()
        self.variables = user_def.variables
        #self._sanitise_quotes()
        # self._replace_all_space()

        self.main_parser(self.content)

        self.content = self.rebuild_content()
        #self._unsanitise_quotes()

        return self.content

    def finder(self, name, c_type=None, c_class=None, c_func=None, p_indent=0):
        print('finder: ', name, len(name))
        print('c_class: ', c_type, c_class, c_func)

        # check name
        if not name:
            return None
        elif name == self.space_char:
            return None
        elif name == (self.space_char * len(name)):
            return None

        # If it is by itself in the file
        if not c_type and not c_class and not c_func and not p_indent:

            if name in self.variables['__main_parent__'][1]:
                return name

            elif name in self.variables['___imports']:
                return name

            else:
                return None

        elif c_class:
            # If func name is set
            if c_func:
                if name in self.variables[c_class][0][c_func]:
                    return name
                # prop can be found inside the __init__
                elif name in self.variables[c_class][0]['__init__']:
                    return name
                # search the general imports
                elif name in self.variables['___imports']:
                    return name
                elif name in self.variables['__main_parent__'][1]:
                    return name
            # if func name is not set
            else:
                if name in self.variables[c_class][0]['__init__']:
                    return name
                elif name in self.variables['___imports']:
                    return name
                elif name in self.variables['__main_parent__'][1]:
                    return name

        # if it is in a function in the file
        elif c_type == 'def':
            if name in self.variables['__main_parent__'][0][c_func]:
                return name
            elif name in self.variables['__main_parent__'][1]:
                return name
            elif name in self.variables['___imports']:
                return name

        else:
            print('name: ', name)
        return

    def main_parser(self, content):
        
        lines = content.split('\r\n')
        self.r_lines_len = len(lines)

        no = -1
        for line in lines:
            no += 1
            # Replace the newline character with its unicode character
            if line == '':
                line = '\u2029'

            self._parse_props(line)
            print('props pars: ', line)
            line = self._start_replace_processes(line)
            print('after replace proc: ', line)
            # mark prop names
            line = self._mark_prop_names(line)
            print('after mark prop names: ', line)
            # mark function names
            line = self._mark_func_names(line)
            print('after mark func names: ', line)
            # Underline unfound
            line = self._mark_unfound(line, no)
            print('after mark unfound: ', line)

            self.lines.append(line)


    def rebuild_content(self):

        string = ''
        for line in self.lines:
            if type(line) == type(''):
                string += line + ''
        return string

    def _mark_func_names(self, line):

        if not line:
            return line

        if 'def</span> ' in line:
            name = line.split('def</span> ')[1].split('(')[0]
            html = user_func_dict['bar'].format(name)
            line = line.replace(name+'(', html)

        return line

    def _mark_prop_names(self, line):
        # mark property that are been referenced
        # narrow down to certain instances

        if not line:
            return line

        if 'class</span>' in line or 'def</span>' in line or ': ' in line:
            pass
        else:
            # split on <span>
            sp_splits = re.split('<span.*?.*?.*?=\s?</span>', line)
            print('sp: ', sp_splits)

            # find those used in brackets
            new_splits = self._find_props_in_brac(sp_splits)
            main_splits = self._separ([sp_splits[-1]])
            print('new: ', new_splits)
            print('main_splits: ', main_splits)
            """a = new_splits[-1].split(' ')
            print('a: ', a)
            # remove empty space chars and commas
            b = [pick.replace(',', '') for pick in a if pick != '' and pick != ',']
            print('b: ', b)
            # remove strings props
            c = [pick for pick in b if "'" not in pick and '"' not in pick]
            print('c: ', c)
            d = [pick.replace('(', '').replace(')', '') for pick in c]
            print('d: ', d)
            e = [pick.replace('{', '').replace('}', '') for pick in d]
            print('e: ', e)
            f = [pick.replace('[', '').replace(']', '') for pick in e]
            print('f: ', f)
            g = [pick for pick in f if not pick.startswith('<span>')]
            print('g: ', g)
            h = [pick for pick in g if pick not in ['-', '+', '/', '*']]
            print('h: ', h)
            i = [pick for pick in h if pick not in ['(', ')', '[', ']', '{', '}']]
            print('i: ', i)
            main_splits = i"""

            # IHandle all in a loop
            for prop in main_splits:
                found = self.finder(prop, c_type=self.curr_type, c_class=self.curr_class, c_func=self.curr_func)
                if found:
                    # mark
                    line = line.replace(found, ref_prop_name['baz'].format(found))

        return line

    def _find_props_in_brac(self, raw_list):

        """
        Gets the property names out of brackets
        and adds them to the property list
        """

        final_list = []
        data = raw_list[-1]

        if '(' in data and ')' in data:
            content = data.split('(')[-1].split(')')[0] # it contains 1+
            final_list.append(content)
        else:
            return raw_list

        return final_list

    def _parse_props(self, line):

        sngl, dobl, line = escape_user_strings(line)
        sgnl_com, dobl_com, line = escape_user_comments(line)

        sp_splits = line.split(' ')
        main_splits = [b for b in sp_splits if b != '']

        # find class
        if re.findall(r'\bclass\b', line):
            self.curr_type = 'class'
            splits = line.split('class ')
            a_split = splits[0]

            indent = 0
            # if all are spaces then its an indent
            if a_split == ' '*len(a_split):
                indent = len(a_split)

            b_split = splits[1]
            if '(' in b_split:
                name = b_split.split('(')[0]
            else:
                name = b_split.split(':')[0].replace(' ', '')

            self.curr_class, self.curr_par_indent = name, indent

        # find def
        if 'def' in main_splits:
            print('\n', '*************')
            print('parse_props: ', main_splits)
            print('\n', '********%%%%%%%%%%%%%%%%')
            self.curr_type = 'def'
            splits = line.split('def ')
            a_split = splits[0]

            # if all are spaces then its an indent
            if a_split == ' '*len(a_split):
                indent = len(a_split)

            b_split = splits[1]
            if '(' in b_split:
                name = b_split.split('(')[0]
            else:
                name = b_split(':')[0].replace(' ', '')

            self.curr_func, self.curr_par_indent = name, indent

        # it is the only thing on the line
        if len(main_splits) == 1:
            if '(' in main_splits[0]:
                pass
            else:
                pass

    def _start_replace_processes(self, line):

        # Replaces
        if not line:
            return line

        for var in self.replace_processes:
            line = self._replace(var, line)
        return line

    def _separ(self, splits):
        print('pre span: ', splits)
        splits = self._add_span_to_list(splits)
        print('after span: ', splits)
        sParen = SplitParenthesis(splits)
        splits = sParen.start()
        print('pre: ', splits)
        splits = self._add_spaces_to_list(splits)
        print('space boy: ', splits)
        return splits

    def _mark_unfound(self, line, no):

        if not line:
            return line
        left_ahead = ""
        equal_sign = fix_span_stat(base_operand_repl.format('='))
        if equal_sign in line:
            junk_s = line.split(equal_sign)
            junky = junk_s[:-1]
            ww = ''
            for x in junky:
                ww += x + '='
            left_ahead = ww[:-1] + equal_sign
            line = junk_s[-1]

        word_splits = []
        # Find if line contains just spaces
        founds = re.findall(r"[A-Za-z0-9`~!@#$%^&*\(\)\[\]-{}_=+/?<,.|>]*", line)
        found = str(founds).replace(', ', '').replace("'", "")
        if found == '[]':
            # Empty
            if (no+1) < self.r_lines_len:
                line = '\u2029'
            else:
                line = ''
        else:
            line += '\u2029'

        """splits = line.split(" ")
        splits = add_splitter(splits, self.space_char)
        print('what is this: ', splits)"""
        splits = [line]
        splits = self._separ(splits)
        """splits = self._add_span_to_list(splits)
        sParen = SplitParenthesis(splits)
        splits = sParen.start()
        splits = self._add_spaces_to_list(splits)"""
        word_splits.extend(splits)
        word_splits_s = word_splits

        no = -1
        content = ""

        # Start with the Marking of the unfound
        for word in word_splits:
            no += 1
            if word.startswith('<span'):
                pass
            elif self._is_string(word):
                word_splits_s[no] = word
            elif word == "\u2029":
                word_splits_s[no] = '\u2029'
            elif word == self.space_char:
                # A space unless its the last entry
                word_splits_s[no] = self.space_char
            elif word == "":
                if (no + 1) == len(word_splits_s):
                    # If it is the last entry probably its not a space
                    word_splits_s.pop()
            elif word in self.escape_parentesis or word in self.operand_types:
                word_splits_s[no] = word
            else:
                stat = '<span style="color: red">' + word + '</span>'
                word_splits_s[no] = stat

        # recompose back into a line
        for each in word_splits_s:
            if each == '\u2029':
                # a space then a break
                content += '\u2029'

            elif each == self.space_char:
                content += self.space_char

            elif each.endswith('\u2029</span>'):
                content += each.replace('\u2029</span>', '</span>\u2029')

            elif each.endswith('\u2029'):
                # a break of line after a modification
                content += each
            else:
                # this should only perhaps for the middle
                content += each

        # Add left ahead back to line
        content = left_ahead + content
        self.content = content
        return content

    def _is_string(self, word):
        if word:
            if word[0] == "'" or word[0] == '"':
                return True

        return False

    def _add_spaces_to_list(self, old_list):
        lister = []

        for l in old_list:
            lister.append(l)

            # we have already splitted on span so this is safe
            if '<span' in l:
                pass
            elif self.space_char == l:
                pass
            else:
                if self.space_char in l:
                    lister.remove(l)
                    one = l.split(self.space_char)
    
                    """no = -1
                    for o in one:
                        no += 1
                        if o == '':
                            one[no] = self.space_char"""

                    # add the space char back
                    # so we have it for the final recomposition
                    one = add_splitter(one, self.space_char)
                    lister.extend(one)

        return lister

    def _add_span_to_list(self, old_list):

        lister = old_list
        for l in old_list:
            if '"</span>' in l or "'</span>" in l:
                continue
            elif "</span>'" in l or '</span>"' in l:
                continue
            elif "'</span>'" in l or '"</span>"' in l:
                continue

            if '</span>' in l:
                lister.remove(l)
                occ = re.findall('<span.*?.*?.*?</span>', l)
                lo = re.split('<span.*?.*?.*?</span>', l)

                no = -1
                for oc in occ:
                    no += 2
                    lo.insert(no, oc)

                lister.extend(lo)
                break

        return lister

    def _replace(self, var, line):

        if var == 'base':
            main_var = self.base_types
            main_dict = self.base_types_dict
            main_func = base_functions
            main_func_dict = base_func_dict

        elif var == 'spaceless':
            main_var = base_operand
            main_dict = base_operand_repl
            line = self._replace_spaceless_var(main_var, main_dict, line)
            return line

        # variable replacement
        line = self._replace_space_var(main_var, main_dict, line)

        # function replacement
        for y in main_func:
            if y in line:
                line = line.replace(y, main_func_dict[y])

        return line

    def _replace_spaceless_var(self, main_var, main_dict, line):

        sngl, dobl, line = escape_user_strings(line)

        # escape unicode characters including space char &nbsp;
        line = escape_unicode(line)

        for x in main_var:
            if x in line and '"'+x+'"' not in line and "'"+x+"'" not in line:
                line = line.replace(x, main_dict.format(x))

        # fix escape for less and greater than symbols
        line = fix_span_stat(line)

        # put back stuff remove because of special chars parsing
        line = put_back_unicode(line)
        line = put_back_user_strings(sngl, dobl, line)

        return line

    def _put_strings_back(self, sngl, dobl, line):
        
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

    def _replace_space_var(self, var, var_dict, line):
        splits = line.split(' ')

        for x in var:
            if x in splits:
                ind = splits.index(x)
                splits[ind] = var_dict.format(x)

        # Add all to string
        string = ""
        for a in splits:
            string += a + " "

        # And back to contents
        line = string[:-1]
        return line

    def _replace_all_space(self):
        # change spaces to unicode &nbsp;
        self.content = self.content.replace(' ', self.space_char)

    def _sanitise_quotes(self):
        lines = self.content.split('\r\n')
        cwq = ""

        for line in lines:
            if '"' in line:
                cwq = '"'
            elif "'" in line:
                cwq = "'"
            else: continue

            pat = cwq + '.*?' + cwq
            matches = re.findall(pat, line)
            if matches:
                for match in matches:
                    fixed = match.replace(" ", "&nbspjeride;")
                    self.content = self.content.replace(match, fixed)

    def _unsanitise_quotes(self):
        self.content = self.content.replace('&nbspjeride;', " ")
