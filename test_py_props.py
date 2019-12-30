import pytest
import os
from vocabulary.voc import Vocabulary

cwd = os.getcwd()
path = os.path.join(cwd, '_tests')


@pytest.mark.parametrize('gi,go', [('_file_props_used_class_itself.py',
                                    '_file_props_used_class_itself_out.txt')])
def test_file_props(gi, go):
    
    # get the in variable
    in_p = os.path.join(path, gi)
    with open(in_p, 'r') as in_h:
        in_b = in_h.read()

    # get the out variable
    out_p = os.path.join(path, go)
    with open(out_p, 'r') as fh:
        outb = fh.read()
        out = outb.replace('\n', '\u2029')

    v = Vocabulary(in_b)
    ret = v.start()

    assert ret == out
