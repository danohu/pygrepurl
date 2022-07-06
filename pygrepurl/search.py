import json
import ctypes
import os
from pygrepurl import util
from roaringbitmap import RoaringBitmap
import re

# We're wrapping a golang library via ctypes, hence a bit of faff
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

def search_trigrams(query, urlstore, tgindex):
    regex = re.compile(query)
    tg_tree = trigrams_from_regex(query)
    bmp = RoaringQuery(tg_tree, tgindex)
    candidates = (urlstore.get(url_id) for url_id in bmp)
    return (c for c in candidates if regex.search(c))

def RoaringQuery(qry, tgindex):
    """
    recursively turn the trigram hierarchy into a set of
    roaringbitmap boolean operations
    return one bitmap representing url_ids that (potentially)
    match the query regex
    """
    # at each level, we have one operation applied to some trigrams
    # which may be supplied immediately, or by recursing into subsections

    # first, special-case the 'everything' and 'nothing' operations
    # special cases for matching everything and matching nothing
    if qry['Op'] == QAll:
        # match everything: create an all-1s bitmap
        full_bm = RoaringBitmap()
        full_bm.flip_range(0, tgindex.cardinality)
        return full_bm
    if qry['Op'] == QNone:
        return RoaringBitmap()

    # now, build up the list of (references to) bitmaps
    bitmaps = [tgindex.maps[tg] for tg in qry['Trigram'] or []]
    for subquery in qry['Sub'] or []:
        bitmaps.append(RoaringQuery(subquery, tgindex))

    # then, apply the operations

    # AND/OR with <2 bitmaps shouldn't happen. But I've not
    # tested, so play safe and handle them
    assert len(bitmaps) > 0
    if len(bitmaps) == 1: 
        return bitmaps[0]
    
    if qry['Op'] == QAnd:
        return bitmaps[0].intersection(*bitmaps[1:])
    if qry['Op'] == QOr:
        return bitmaps[0].union(*bitmaps[1:])

    
