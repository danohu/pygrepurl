# Regular expression URL search

Regular expressions are great. Except, mostly, you can't use them on the internet. The search engines of the world have mostly decided that implementing regular expression search is just too hard.

Except -- if you just get the architecture right, regular expression search is easier than you might think.

This library is here to demonstrate that. I've used it to allow regex search across 50 million URLs on a single not-very-powerful machine. The indices are small enough to fit in RAM, and search happens in a matter of milliseconds.

# How it works

It's built around a trigram index. Each url gets broken down into 3-letter chunks. So example.com becomes [exa,xam,amp,mpl,ple,le.,e.c,.co,com]. I also associate an integer ID with each URL. Then I can create for each trigram, a record of all the URLs it appears in.

At this point, I'd be able to find all the URLs that contain a 3-letter string. OMG FTW, etc.

But when it comes to search, I want to be able to work with combinations of trigrams. I'm going to break down the regex to figure out what trigrams it must contain, in what combination. Let's say the query is 'exam.*(com|org)'. That means I know it needs to contain 'exa', 'xam' and either 'com' or 'org'.

In other words, I need to perform set operations -- unions and intersections -- on the trigram indices. To enable this I store the indices as bitmaps. One bit in each index corresponds to each url -- making sure that the URL ids are sequential integer counting from zero. Say that example.com is the 500,000th url I index -- I flip bit number 500,000 to 1 in each of the indices of [exa,xam,amp,mpl,ple,le.,e.c,.co,com].

Now when I get the query above, I find the bitwise intersection of the 'exa' and 'xam' indices, and intersect that with the union of 'com' and 'org'. Then I read off the positive bits, and pull out the URLs corresponding to those IDs.

Finally, I need to check which of the URLs really match the query. This is where we need to turn to a real regex engine, something that can figure out why 'xamorgexa.fi' shouldn't match. I just feed them into the python regex engine.

Of course, it takes a few more tricks along the way, to make sure the performance is good enough to keep it usable. I can't afford to store the complete bitmaps -- each of them is sparse, and so it's better to use some kind of run-length encoding. I chose to use [roaring bitmaps](http://roaringbitmap.org/), though other forms of RLE would provide similar benefits.

As well as keeping the bitmaps small enough to (just about) fit in RAM, this speeds up the set operations. If we have big runs of 1 or 0, we can operate on them without needing to look at every individual bit. To maximize the benefits of this, I want to make the run lengths as bunched-up as possible. I sort the URLs before assigning them IDs, meaning that sequential bits will have at least their _start_ in a similar position. [I could probably do even better if I ordered by similarity rather than just prefix, but I'll leave that for the future].

The mapping of IDs to URLs is also compressed. I'm using a library called [marisa-trie](https://marisa-trie.readthedocs.io/) for this. It's one of many trie variants, and keeps to the odd tradition that every trie should have a woman's name (say hello, Judy and Patricia!). I've not figured out quite what's happening under the hood  -- much of the documentation is in Japanese -- but it has two very useful properties in comparison to other tries. Firstly, I can look up any item by an integer index, and secondly, it is highly compressed. I would actually have been content with reading URLs from disk, but marisa is small enough that I can pull the URLs into RAM as well.

For the breakdown of regexes into trigrams, I was able to take advantage of some code written by Russ Cox for Google code search. It's written in Go, and -- despite some work at [Mozilla](https://github.com/mozilla/dxr/blob/master/dxr/trigrammer.py) -- there isn't an alternative in python. So I wrote a little wrapper around his code in Go, exported it as a .so, and then called out to that from python using ctypes. A bit of extra complexity in the build process, but much simpler than writing my own regex parser!

## Installation

Get going with:
	
	pip install -r requirements.txt
	python setup.py develop

However, there is also an external dependency on a go library. I've taken some of Russ Cox's trigram-index code from https://github.com/google/codesearch and wrapped it in a python interface.

If you're lucky, and running Debian/Ubuntu, the included .so *might* work. If not, you'll need to:

	go get github.com/google/codesearch/index
	cd pygrepurl
	go build -buildmode=c-shared -o trigrams.so trigrams.go


## Running with sample data

You can start a basic command-line interface with 

	pygrepurl serve

This will use a small dataset of ~12,000 URLs. Type a regex to stdin, and you'll see matching URLs

## Building your own index

More useful is to build your own database of URLs. pygrepurl expects you to feed it a bunch of files containing URLs, one per line, optionally gzipped. 

Common crawl is a good starting-point. You can use their [url index client](https://github.com/ikreymer/cdx-index-client) to download, for example, all URLs in the .de TLD:

	./cdx-index-client.py "*de" --fl url  -d /data/commoncrawl -z -o de_

This will give you a bunch of gzipped files like /data/commoncrawl/de_2676.gz

Then use the pygrepurl cli to import these files:

	pygrepurl load /data/commoncrawl/*gz

...and make yourself some tea.



