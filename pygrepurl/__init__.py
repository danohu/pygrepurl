# -*- coding: utf-8 -*-
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

from pygrepurl.trigram_extract import QAll,QNone,QAnd,QOr, trigrams_from_regex
from roaringbitmap import RoaringBitmap
    


def search_trigrams(query, urlstore, tgindex):
    tg_tree = trigrams_from_regex(query)
    bmp = RoaringQuery(tg_tree, tgindex)
    return [urlstore.get(url_id) for url_id in bmp]
    #for url_id in bmp:
    #    yield urlstore.get(url_id)

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
    bitmaps = [tgindex.maps[tg] for tg in qry['Trigram']]
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

    
