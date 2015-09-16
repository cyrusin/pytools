#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import operator

def get_data():
    return random.sample(range(10), 3)


def consumer():
    running_sum = 0
    data_items_seen = 0

    while 1:
        print 'waiting items to consume'
        data = yield
        data_items_seen = data_items_seen + len(data)
        running_sum = reduce(operator.add, data, running_sum)
        print 'consume: the sum now is:', running_sum


def producer(consumer):
    while True:
        data = get_data()
        print 'produce: ', data
        consumer.send(data)
        yield


if __name__ == '__main__':
    c = consumer()
    c.send(None)
    p = producer(c)

    for _ in xrange(10):
        next(p)
