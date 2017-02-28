#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pygrepurl.skeleton import fib
from pygrepurl.spl import START_URL, END_URL
from pygrepurl.spl import split_trigram, runimport
from pygrepurl import spl

__author__ = "Dan O'Huiginn"
__copyright__ = "Dan O'Huiginn"
__license__ = "none"



def test_split_trigram():
    url = "example.com"
    expected =  [START_URL + "ex", "exa", "xam", "amp", "mpl", "ple", "le.", "e.c", ".co", "com", "om" + END_URL]
    result = list(split_trigram(url))
    assert len(result) == len(expected)
    assert all(result[i] == expected[i] for i in range(len(expected)))

def test_runimport():
    runimport(["testdata.txt",])

def test_urlstore():
    ms = spl.MemoryURLStore()
    for i, el  in enumerate(['aa', 'bbb', 'c', 'd']):
        idx = ms.addURL(el, [])
        assert ms.getURL(idx) == el
