#!/usr/bin/env python
# -*- coding:utf-8 -*-
u'''固定线程数的线程池实现
'''
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
                task = self._tasks.get(block=True, timeout=self._timeout)
            except Queue.Empty:
                continue
            #if current thread is dismissed when blocking
            #exit and put the todo task back to the task queue
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


class Task(object):
    u'''封装原函数和参数
    Attributes:
    @ID: unique task id
    @do: raw function
    @args & kwargs: raw params of raw function
    @error: status when calling func(*args, **kwargs)
    @exception_handler: <function>, use `exception_handler(exception)` to handle exception
    '''
    def __init__(self, func, args=None, kwargs=None, exception_handler=None):
        self.ID = id(self)
        self.do = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.error = False
        self.handle_exception = exception_handler or self._handle_exception

    def _handle_exception(self, e):
        pass


class ThreadPool(object):
    u'''线程池
    '''
    def __init__(self, worker_num, timeout=2):
        self.task_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.workers = []
        self.tasks = dict()
        self.all_task_done = False
        self.create_workers(worker_num, timeout)

    def create_workers(self, worker_num, timeout):
        for i in range(worker_num):
            self.workers.append(Worker(self.task_queue, self.result_queue, timeout))

    def submit(self, task, block=True, timeout=None):
        self.task_queue.put(task, block, timeout)
        self.tasks[task.ID] = task

    def poll(self):
        while 1:
            if not self.tasks:
                self.all_task_done = True
                break
            task, result = self.result_queue.get(block=True)
            try:
                if task.error:
                    task.handle_exception(result)
            except:
                pass
            del self.tasks[task.ID]

    def join(self):
        for w in self.workers:
            w.dismiss()
        for w in self.workers:
            w.join()


if __name__ == "__main__":
    def do_work(i):
        print "One thread is processing task: %s\n" % i

    MAX_WORKERS = 3
    print "Create thread pool with %s threads" % MAX_WORKERS

    pool = ThreadPool(MAX_WORKERS)
    for i in range(100):
        r = Task(do_work, args=[i])
        pool.submit(r)
    pool.poll()
    pool.join()

    print "All task done"
