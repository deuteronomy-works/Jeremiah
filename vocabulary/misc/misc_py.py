# -*- coding: utf-8 -*-

class SplitParenthesis():
    
    
    def __init__(self, entry):
        self.data = entry # expects entry to be a list
        self.parenthesis = ['(', ')', '[', ']', '{', '}']

    def start(self):
        self._check(0)
        return self.data

    def _spliter(self, conts, chars):

        splits = conts.split(chars)
        newer = []
        no = -1
        for x in splits:
            no += 1
            if no == len(splits) - 1:
                newer.append(x)
                break
            newer.append(x)
            newer.append(chars)
    
        return newer
    
    def _insert_list(self, ind, par, child):

        inde = ind
        for x in child:
            par.insert(inde, x)
            inde += 1
    
    def _find_par(self, worde, w_ind):

        for x in self.parenthesis:
            if x in worde and x != worde:
                d = self._spliter(worde, x)
                self.data.pop(w_ind)
                self._insert_list(w_ind, self.data, d)
                return True

        return False
    
    def _check(self, ind):
        if ind == len(self.data):
            return
        else:
            if self._find_par(self.data[ind], ind):
                self._callback(ind)
            else:
                self._callback(ind+1)
    
    def _callback(self, ind):
        self._check(ind)
