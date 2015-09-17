#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''Some tools used in str.
just `import str_util` to use any of this.
'''

import collections


class FrequencyStr(str):
    u'''相同词频字符串相等
    >>> a = FrequencyStr('abb')
    >>> b = FrequencyStr('bba')
    >>> a is b
    >>> False
    >>> a == b
    >>> True
    >>> hash(a)
    >>> 1453079729188098210
    >>> hash(b)
    >>> 1453079729188098210
    >>> a
    >>> 'abb'
    >>> b
    >>> 'bba'
    '''
    @property
    def normalized(self):
        try:
            return self._normalized
        except AttributeError:
            self._normalized = normalized = ''.join(sorted(collections.Counter(self).elements()))
            return normalized

    def __eq__(self, other):
        return self.normalized == other.normalized

    def __hash__(self):
        return hash(self.normalized)


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
