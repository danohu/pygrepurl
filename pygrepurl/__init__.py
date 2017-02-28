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
