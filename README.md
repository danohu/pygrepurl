# Regular expression URL search

Search a billion URLs by regular expression.
On a single machine. In RAM.

## Installation

The usual `python setup.py install` will handle the python dependencies. It was written in python3.5, and probably won't work with python 2.

However, there is also an external dependency on a go library. I've taken some of Russ Cox's trigram-index code from https://github.com/google/codesearch and wrapped it in a python interface.

If you're lucky, and running Debian/Ubuntu, the included .so *might* work. More likely, you'll need to:

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
cd s


## Architecture

