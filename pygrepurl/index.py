from roaringbitmap import RoaringBitmap
from collections import defaultdict
from pygrepurl import util
import gzip
import os
import marisa_trie
import pickle

FILENAMES = {
    'urlstore': 'urlstore.data',
    'trigrams': 'trigrams.data'
    }

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

    def persist(self, datadir):
        fn = os.path.join(datadir, FILENAMES['trigrams'])
        with open(fn, 'wb') as fh:
            return pickle.dump(self,fh)

    @classmethod
    def load(cls, datadir):
        fn = os.path.join(datadir, FILENAMES['trigrams'])
        with open(fn, 'rb') as fh:
            return pickle.load(fh)
        
class URLStore:

    def persist(self, datadir):
        fn = os.path.join(datadir, FILENAMES['urlstore'])
        with open(fn, 'wb') as fh:
            return pickle.dump(self,fh)

    @classmethod
    def load(cls, datadir):
        fn = os.path.join(datadir, FILENAMES['urlstore'])
        with open(fn, 'rb') as fh:
            return pickle.load(fh)

class MarisaURLStore(URLStore):
    """
    Static, space-efficient, persistable version
    
    You cannot incrementally build this, so use the MemoryURLStore first
    """

    def __init__(self, urls=None):
        self.trie = marisa_trie.Trie(urls or [])

    def add(self, url):
        raise NotImplementedError

    def get(self, url_id):
        return self.trie.restore_key(url_id)

    def items(self):
        return self.trie.iteritems()
        

class MemoryURLStore(URLStore):

    def __init__(self, urls=None):
        self.urls = urls or []

    def add(self, url):
        """returns an index that can be used to get the url later"""
        self.urls.append(url)
        return len(self.urls) -1

    def get(self, _id):
        """Will raise IndexError on non-existent url"""
        return self.urls[_id]

    def to_marisa(self):
        return MarisaURLStore(self.urls)

    def items(self):
        # odd order to keep in line with the Marisa Trie version
        return ((v,k) for (k,v) in enumerate(self.urls))
    
def runimport(files):
    urlstore = MemoryURLStore()
    tgindex = BitIndex()
    for fn in files:
        openfunc = gzip.open if fn.endswith('gz') else open
        with openfunc(fn, 'rb') as inf:
            lines_to_urlstore(inf, urlstore)
    marisa = urlstore.to_marisa()
    del(urlstore)
    for url, url_id in marisa.items():
        trigrams = util.split_trigrams(url)        
        tgindex.add(url_id, trigrams)    
    return marisa, tgindex

def lines_to_urlstore(it, urlstore):
    for i, line in enumerate(it):
        line = line.decode('utf-8')
        url = util.prepare_url(line)
        urlstore.add(url)
        #if i > 250: break
