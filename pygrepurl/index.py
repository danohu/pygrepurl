from roaringbitmap import RoaringBitmap
from collections import defaultdict
from pygrepurl import util

class BitIndex:

    def __init__(self):
        self.maps = defaultdict(RoaringBitmap)
        # keep track of how many items there are, so we can
        # match ALL without returning billions of nonexisting keys
        self.cardinality = 0

    def add(self, url_id, trigrams):
        '''
        add an url to the index: set the bit at the urls ID for every
        trigram it contains
        '''
        for trigram in trigrams:
            self.maps[trigram].add(url_id)
            self.cardinality = max(self.cardinality, url_id)


class MemoryURLStore:

    def __init__(self):
        self.urls = []

    def add(self, url):
        """returns an index that can be used to get the url later"""
        self.urls.append(url)
        return len(self.urls) -1

    def get(self, _id):
        """Will raise IndexError on non-existent url"""
        return self.urls[_id]


def runimport(files):
    urlstore = MemoryURLStore()
    tgindex = BitIndex()
    for fn in files:
        with open(fn, 'r') as inf:
            for line in inf:
                url = util.prepare_url(line)
                trigrams = util.split_trigrams(url)
                url_id = urlstore.add(url)
                tgindex.add(url_id, trigrams)
    return urlstore, tgindex
