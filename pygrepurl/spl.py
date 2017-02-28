import urllib

START_URL = "\x02"
END_URL = "\x03"

def split_trigram(s):
    """
    return all 3-letter substrings of the input
    also include substrings with start/end markers
    """
    # 2-letter input won't occur in our data,
    # and would need special handling
    s = prepare_url(s)
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


# String Functions
"""
We need to be strict about character classes
- everything lowercase
- strip http:// etc
"""
valid_chars = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;=`.%")
special_chars = [START_URL, END_URL]

def prepare_url(url):
    url = url.lower()
    if not all(x in valid_chars for x in url):
        url = urllib.quote(url)
    url = START_URL + url + END_URL
    assert len(url) > 2
    return url
