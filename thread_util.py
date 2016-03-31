#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import Queue

class Worker(threading.Thread):
    u'''工作线程
    '''
    def __init__(self, task_queue, result_queue, timeout, **kwargs):
        super(Worker, self).__init__(**kwargs)
        self.setDaemon(True)
        self._tasks = task_queue
        self._results = result_queue
        self._timeout = timeout
        self._dismissed = threading.Event()
        self.start()

    def run(self):
        while 1:
            if self._dismissed.is_set():
                break
            try:
                #block until Queue is readable or timeout
                task = self._tasks.get(True, self._timeout)
            except Queue.Empty:
                continue
            #重新判断是否需要dismiss(blocking时也许dismissed)
            #确保可以及时响应dismiss
            if self._dismissed.is_set():
                self._tasks.put(task)
                break

            try:
                result = task.do(*task.args, **task.kwargs)
                self._results.put((task, result))
            except Exception as e:
                task.error = True
                self._results.put((task, e))

    def dismiss(self):
        self._dismissed.set()


