from six.moves.urllib import parse


START_URL = "\x02"
END_URL = "\x03"

def split_trigrams(s):
    """
    return all 3-letter substrings of the input
    also include substrings with start/end markers
    """
    # 2-letter input won't occur in our data,
    # and would need special handling
    s = prepare_url(s)
    s = START_URL + s + END_URL
    return [s[i:i+3] for i in range(len(s)-2)]

# String Functions
"""
We need to be strict about character classes
- everything lowercase
- strip http:// etc
"""
valid_chars = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;=`.%")
special_chars = [START_URL, END_URL]

def prepare_url(url):
    url = url.strip().lower()
    return url
    if not all(x in valid_chars for x in url):
        url = parse.quote(url)
    # assert len(url) > 2
    return url
