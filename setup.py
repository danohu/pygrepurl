#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for pygrepurl.

    This file was generated with PyScaffold 2.5.7, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

from setuptools import setup

setup(
    name='pygrepurl',
    version='0.1',
    py_modules=['yourscript'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pygrepurl=pygrepurl:cli
    ''',
)
