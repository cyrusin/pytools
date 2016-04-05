import heapq

class Item(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item: {}'.format(self.name)


class PriorityQueue(object):
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        if not self.empty():
            return heapq.heappop(self._queue)[-1]
        else:
            return None

    def empty(self):
        return True if not self._queue else False

    def __len__(self):
        return len(self._queue)

    def __iter__(self):
        return iter(self._queue)

    def top(self):
        return self._queue[0] if not self.empty() else None

if __name__ == '__main__':
    pq = PriorityQueue()
    pq.push('foo', 2)
    pq.push('bar', 3)
    pq.push('jj', 1)
    pq.push('ab', 9)
    pq.push('da', 4)

    print "length of queue: ", len(pq)
    print "top: ", pq.top()
    for item in pq:
        print item
    while not pq.empty():
        print pq.pop()
