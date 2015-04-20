#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Some useful tools based on itertools module
url: https://docs.python.org/2/library/itertools.html
"""

import itertools

def take(n, iterable):
    '''Return first n items of the iterable as a list'''
    return list(itertools.islice(iterable, n))

def tabulate(function, start=0):
    '''Return function(0), function(1), ...'''
    return itertools.imap(function, itertools.count(start))
