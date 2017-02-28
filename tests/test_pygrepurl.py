#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pygrepurl.util import START_URL, END_URL, split_trigrams
from pygrepurl.index import runimport, MemoryURLStore
from pygrepurl.search import search_trigrams

__author__ = "Dan O'Huiginn"
__copyright__ = "Dan O'Huiginn"
__license__ = "none"



def test_split_trigrams():
    url = "example.com"
    expected =  [START_URL + "ex", "exa", "xam", "amp", "mpl", "ple", "le.", "e.c", ".co", "com", "om" + END_URL]
    result = list(split_trigrams(url))
    assert len(result) == len(expected)
    assert all(result[i] == expected[i] for i in range(len(expected)))

def test_runimport():
    runimport(["tests/testdata.txt",])

def test_urlstore():
    ms = MemoryURLStore()
    for i, el  in enumerate(['aa', 'bbb', 'c', 'd']):
        idx = ms.add(el)
        assert ms.get(idx) == el

def test_retrieveurl():
    urlstore, tgindex = runimport(['tests/testdata.txt'])
    searchterm, expected = ".*fabians.*ELect...l.*", ["http://www.fabians.org.uk/under-corbyns-electoral-plan-prospects-for-victory-look-bleak/"]
    actual = search_trigrams(searchterm, urlstore, tgindex)
    assert(list(actual) == expected)
