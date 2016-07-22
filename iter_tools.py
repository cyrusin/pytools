#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Some useful tools based on itertools module
url: https://docs.python.org/2/library/itertools.html
"""

import itertools
import operator
import collections

def take(n, iterable):
    '''Return first n items of the iterable as a list'''
    return list(itertools.islice(iterable, n))

def tabulate(function, start=0):
    '''Return function(0), function(1), ...'''
    return itertools.imap(function, itertools.count(start))

def nth(iterable, n, default=None):
    '''Return the nth element of iterable'''
    return next(itertools.islice(iterable, n, None), default)

def quantify(iterable, pred=bool):
    '''Count how many times the predicate is True'''
    return sum(itertools.imap(pred, iterable))

def padnone(iterable):
    '''Returns the iterable's elements and None indefinitely.'''
    return itertools.chain(iterable, itertools.repeat(None))

def ncycles(iterable, n):
    '''Returns the elements of iterable for n times'''
    return itertools.chain.from_iterable(itertools.repeat(tuple(iterable), n))

def dotproduct(vec1, vec2):
    return sum(itertools.imap(operator.mul, vec1, vec2))

def flatten(listOfLists):
    '''Flatten one level of list'''
    return itertools.chain.from_iterable(listOfLists)

def repeatfunc(function, times=None, *args):
    '''Repeat calls with specified times and args'''
    if times is None:
        return itertools.starmap(function, itertools.repeat(args))
    return itertools.starmap(function, itertools.repeat(args, times))

def pairwise(iterable):
    '''s -> (s[0], s[1]), (s[1], s[2]),...'''
    iter_0, iter_1 = itertools.tee(iterable)
    next(iter_1, None)
    return itertools.izip(iter_0, iter_1)

def grouper(iterable, n, fillvalue=None):
    '''grouper("abcdefg", 3, 'x') -> 'abc', 'edf', "gxx"'''
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def group_adjacent(lst, k):
    u'''Generate a new list based on `lst`
    such as:
    lst = [0, 1, 2, 3, 4, 5]
    group_adjacent(lst, 2) -> [(0, 1), (2, 3), (4, 5)]
    '''
    return zip(*([iter(lst)] * k))

def unique_everseen(iterable, key=None):
    '''List items unique ever seen, preserving order'''
    seen = set()
    seen_add = seen.add
    if key is None:
        for item in itertools.ifilterfalse(seen.__contains__, iterable):
            seen_add(item)
            yield item
    else:
        for item in iterable:
            k = key(item)
            if k not in seen:
                seen_add(k)
                yield item

def iter_except(func, exception, first=None):
    '''Call a function repeatedly until an exception is raised.
    such as:
    dict_pop_iter = iter_except(d.popitem, KeyError)
    '''
    try:
        if first is not None:
            yield first()
        while 1:
            yield func()
    except exception:
        pass

def n_grams(lst, n):
    '''Return new list based on `lst`
    Such as:
    lst=[1, 2, 3, 4, 5, 6]
    n_grams(lst, 2) -> [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
    '''
    return zip(*([iter(lst[i:]) for i in range(n)]))

def switch_kv(d):
    '''switch_kv(dict) -> dict, but `key:value` is switched by input dict
    '''
    return dict(zip(d.values(), d.keys()))

def remove_dup_items_ordered(lst):
    '''such as: [1, 2, 2, 6, 3, 1, 4, 3] -> [1, 2, 6, 3, 4]
    '''
    return collections.OrderedDict.fromkeys(lst).keys()

class Alphabet(object):
    '''iterable object that give you alphabet with the number you want.
    Such as:
        Alphabet(27, cap=True) -> A, B, C, ...Z, A
        Alphabet(28, cap=True) -> A, B, C, ...Z, A, B
        Alphabet(28, cap=False) -> a, b, c, ...z, a, b
        Alphabet(28) -> a, b, c, ...z, a, b
      
    '''
    def __init__(self, n, cap=False):
        self.stop = n
        self.value = 0
        if cap:
            self.alph = [chr(i) for i in xrange(65, 91)]
        else:
            self.alph = [chr(i) for i in xrange(97, 123)]
        self.alph_length = len(self.alph)

    def __iter__(self):
        return self

    def next(self):
        if self.value == self.alph_length:
            self.value = 0
            self.stop = self.stop - self.alph_length

        if self.value >= self.stop:
            raise StopIteration

        x = self.alph[self.value]
        self.value = self.value + 1
        return x
