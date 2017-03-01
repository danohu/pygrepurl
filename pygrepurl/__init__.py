# -*- coding: utf-8 -*-

import click
import sys

from pygrepurl.search import search_trigrams
from pygrepurl.util import prepare_url
from pygrepurl import index
import os

@click.group()
def cli():
    pass


class Searcher:
    """
    Wrapper suitable for import from other code
    """

    def __init__(self, datadir = None):
        self.datadir = datadir or os.path.dirname(__file__) + '/../data/'
        self.urlstore = index.MemoryURLStore.load(self.datadir)
        self.tgindex = index.BitIndex.load(self.datadir)

    def search(self, searchterm):
        query = prepare_url(searchterm)
        return search_trigrams(query, self.urlstore, self.tgindex)

@cli.command()
@click.option('--datadir', default=os.path.dirname(os.path.abspath(__file__)) + '/../data/')
@click.argument('files', nargs=-1)
def load(files, datadir):
    us, tg = index.runimport(files)
    us.persist(datadir)
    tg.persist(datadir)


@cli.command()
@click.option('--datadir', default=os.path.dirname(os.path.abspath(__file__)) + '/../data/')
def serve(datadir):
    urlstore = index.MemoryURLStore.load(datadir)
    tgindex = index.BitIndex.load(datadir)
    for line in sys.stdin:
        line = prepare_url(line)
        for match in search_trigrams(line, urlstore, tgindex):
            sys.stdout.write(match + '\n')
        

if __name__ == '__main__':
    cli()
