START_URL = "\x02"
END_URL = "\x03"

def split_trigram(s):
    """
    return all 3-letter substrings of the input
    also include substrings for the start and end, containing 
    """
    # 2-letter input won't occur in our data,
    # and would need special handling
    assert len(s) > 2
    s = START_URL + s + END_URL
    return [s[i:i+3] for i in range(len(s)-2)]


def runimport(files):
    for fn in files:
        pass


class MemoryURLStore:

    def __init__(self):
        self.urls = []

    def addURL(self, url, trigrams):
        """returns an index that can be used to get the url later"""
        self.urls.append(url)
        return len(self.urls) -1

    def getURL(self, _id):
        """Will raise IndexError on non-existent url"""
        return self.urls[_id]
