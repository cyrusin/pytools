#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''some useful tools that can be added in your coding with function
'''

import functools


# decorator used in function call count
def call_counter(func):
    '''A decorator used in counting how many times your function is called.
    Use like this:
            >> @call_counter
            >> def my_function(...)
                ...
            >>my_function(...)
            >>my_function(...)
            >>my_function.call_count
            >>2

    '''
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        _wrapper.call_count += 1
        return func(*args, **kwargs)
    _wrapper.call_count = 0
    return _wrapper


