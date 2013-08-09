#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''some useful tools that can be added in your Object-Oriented coding
'''

#Singleton design pattern
def singleton(cls):
    '''
    I need singleton design pattern.
    Use this decorator.
    Usage:
        import oop_utils
        ...
        @oop_utils.singleton
        class MySingletonClass(...):
            ...
    '''
    def wrapper(*args, **kwargs):
        obj = getattr(cls, "__instance__", None)
        if not obj:
            obj = cls(*args, **kwargs)
            cls.__instance__ = obj
        return obj
    return wrapper

