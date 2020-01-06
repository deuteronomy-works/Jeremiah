# -*- coding: utf-8 -*-

base_types = ['if', 'property', 'elif', 'else', 'for', 'while',
              'class', 'def', 'with', 'as', 'in', 'import', 'from', 'and']

base_operand = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', ';', ':', ',', '<', '.', '>','/', '?']

data_types = ['True', 'False', 'None']

base_functions = ['print(', 'list(', 'str(', 'bytes(', 'dict(', 'set(', 'tuple(',
                  'len(', 'format(', 'open(']

base_operand_repl = "[[span]]{}[[jeridespan]]"

base_types_repl = "<span>{}</span>"

base_types_dict = {'if': "<span>if</span>", 'property': "<span>property</span>",
                   'elif': "<span>elif</span>", 'else': "<span>else</span>",
                   "for": "<span>for</span>", 'while': "<span>while</span>",
                   'class': "<span>class</span>", 'def': "<span>def</span>",
                   'with': "<span>with</span>", 'as': "<span>as</span>",
                   'in': "<span>in</span>", 'import': "<span>import</span>",
                   'from': "<span>from</span>", 'and': "<span>and</span>"}

base_func_dict = {'print(': "<span>print</span>(", 'list(': "<span>list</span>(",
                  'str(': "<span>str</span>(", 'bytes(': "<span>bytes</span>(",
                  'dict(': "<span>dict</span>(", 'set(': "<span>set</span>(",
                  'tuple(': "<span>tuple</span>(", 'len(': "<span>len</span>(",
                  'format(': "<span>format</span>(", 'open(': "<span>open</span>("}

