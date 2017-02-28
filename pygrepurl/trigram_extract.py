# Wrapper around Russ Cox's code to convert a regex into trigrams
# see:
# * https://github.com/google/codesearch/blob/master/index/regexp.go
# * https://swtch.com/~rsc/regexp/regexp4.html

import json
import ctypes
import os
sopath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + 'trigrams.so'

trig = ctypes.cdll.LoadLibrary(sopath)

trig.Trigrams.restype = ctypes.c_char_p
trig.Trigrams.argtypes = [ctypes.c_char_p]

QAll,QNone,QAnd,QOr = (0,1,2,3)
# consts from https://github.com/google/codesearch/blob/master/index/regexp.go

def trigrams_from_regex(rgx):
    trgms = trig.Trigrams(rgx.encode('utf-8'))
    trgms = trgms.decode('utf-8')
    return json.loads(trgms)
