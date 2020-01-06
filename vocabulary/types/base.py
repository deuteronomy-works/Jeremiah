# -*- coding: utf-8 -*-

base_types = ['if', 'property', 'elif', 'else', 'for', 'while',
              'class', 'def', 'with', 'as', 'in', 'import', 'from', 'and']

base_operand = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', ';', ':', ',', '<', '.', '>','/', '?']

data_types = ['True', 'False', 'None']

base_functions = ['print(', 'list(', 'str(', 'bytes(', 'dict(', 'set(', 'tuple(',
                  'len(', 'format(', 'open(']

base_operand_repl = "[[span]]{}[[jeridespan]]"

base_types_repl = "[[span]]{}[[jeridespan]]"

base_func_dict = {'print(': "<span>print</span>(", 'list(': "<span>list</span>(",
                  'str(': "<span>str</span>(", 'bytes(': "<span>bytes</span>(",
                  'dict(': "<span>dict</span>(", 'set(': "<span>set</span>(",
                  'tuple(': "<span>tuple</span>(", 'len(': "<span>len</span>(",
                  'format(': "<span>format</span>(", 'open(': "<span>open</span>("}

