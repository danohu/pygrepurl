# Wrapper around Russ Cox's code to convert a regex into trigrams

import json
import ctypes
trig = ctypes.cdll.LoadLibrary('./trigrams.so')

trig.Trigrams.restype = ctypes.c_char_p
trig.Trigrams.argtypes = [ctypes.c_char_p]


def trigrams_from_regex(rgx):

    trgms = trig.Trigrams(rgx.encode('utf-8'))
    trgms = trgms.decode('utf-8')
    return json.loads(trgms)
