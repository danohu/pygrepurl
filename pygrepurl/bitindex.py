from roaringbitmap import RoaringBitmap


class BitIndex:

    def __init__(self, capacity):
        """
        capacity: number of items we can index.
        """
        self.maps = defaultdict(RoaringBitmap)

    def add(self, url_id, trigrams):
        '''
        add an url to the index: set the bit at the urls ID for every
        trigram it contains
        '''
        for trigram in trigrams:
            self.maps[trigram].add(url_id)
