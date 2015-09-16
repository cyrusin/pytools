#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@author:cyrusin
'''This module is used when you want to process file fast.

With coroutine and yield expression, we can use it just like pipe, and 
this way of pipe-like will gain high performance.

Use it like this:
    from file_processing import *
    #you can replace printer() with any function defined like printer()
    data_stream = finder(opener(reader(grep("pattern_you_need",printer())))
    data_stream.send(('dir_name', 'specific name pattern'))
    data_stream.close()
'''
import os
import fnmatch
import gzip
import bz2
import sys

def coroutine(func):
    '''coroutine(func)

    A decorator used on one function with "something=(yield)" in it.
    And the function is obviously used in coroutine.
    Adding this decorator can avoid forgeting running "func.next()" first.
    '''
    def start_func(*args, **kwargs):
        gen_obj = func(*args, **kwargs)
        gen_obj.next()
        return gen_obj
    return start_func

@coroutine
def finder(receiver):
    while True:
        root_dir, pattern = (yield)
        for path, dirname, filelist in os.walk(root_dir):
            for name in filelist:
                if fnmatch.fnmatch(name, pattern):
                    receiver.send(os.path.join(path, name))

@coroutine
def opener(receiver):
    while True:
        name = (yield)
        if name.endswith(".gz"):
            f = gzip.open(name)
        elif name.endswith(".bz2"):
            f = bz2.BZ2File(name)
        else:
            f = open(name)
        receiver.send(f)

@coroutine
def reader(receiver):
    while True:
        f = (yield)
        for line in f:
            receiver.send(line)

@coroutine
def grep(pattern, receiver):
    while True:
        line = (yield)
        if pattern in line:
            receiver.send(line)

@coroutine
def printer():
    while True:
        line = (yield)
        sys.stdout.write(line)

