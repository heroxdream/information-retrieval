__author__ = 'hanxuan'

from Queue import PriorityQueue

from collections import defaultdict

import multiprocessing as mp

from Utils.ulog import log

import time

import random


class BackQueue(object):
    def __init__(self, time_span):
        self.domain_queues = defaultdict(PriorityQueue)
        self.time_stack = dict()
        self.domain_time_span = time_span
        self._size = 0
        self.lock = mp.Lock()
        log.info('BACK_QUEUE_TIME_SPAN: {} ms'.format(self.domain_time_span))

    def pop(self, domain):
        with self.lock:
            self._size -= 1
            return self.domain_queues[domain].get()[1]

    def push(self, domain, tpl):
        with self.lock:
            self._size += 1
            self.domain_queues[domain].put(tpl)

    def time_stack_set(self, domain):
        with self.lock: self.time_stack[domain] = time.time() * 1000

    def domain_count(self):
        return len(self.domain_queues)

    def size(self):
        return self._size

    def push_one(self, domain, tuple_value):
        if domain not in self.domain_queues:
            self.time_stack_set(domain)
            log.debug('time_stack: {}'.format(self.time_stack))
        self.push(domain, tuple_value)
        log.debug('domain: {}'.format(self.domain_queues))

    def pop_one(self, domain):
        if self.domain_queues[domain].empty():
            with self.lock:
                del self.domain_queues[domain]
                del self.time_stack[domain]
            return None
        else:
            url = self.pop(domain)
            self.time_stack_set(domain)
            return url

    def push_out(self):
        if self.size() == 0:
            log.info('NO URL in BACK QUEUE, sleep {} seconds'.format(1))
            time.sleep(1)
            return None

        current_ms = time.time() * 1000
        keys = sorted(self.time_stack.keys(), key=lambda *args: random.random())
        for domain in keys:
            if current_ms - self.time_stack[domain] > self.domain_time_span:
                url = self.pop_one(domain)
                log.debug('url: {} retrieved from back_queue'.format(url))
                return url


if __name__ == '__main__':
    from Crawl.MemShareManager import MemShareManager

    mgr = MemShareManager()
    mgr.start()
    queue = mgr.BackQueue(1000)

    queue.push_one('google', (1, 'music.google'))
    queue.push_one('google', (7, 'doc.google'))
    queue.push_one('google', (5, 'book.google'))
    queue.push_one('google', (2, 'video.google'))
    queue.push_one('facebook', (2, 'video.facebook'))

    print queue.pop_one('google')
    print queue.pop_one('google')
    print queue.pop_one('google')
    print queue.pop_one('facebook')
    print queue.pop_one('facebook')

    # print queue.domain_queues
