__author__ = 'hanxuan'

from Queue import PriorityQueue

from collections import defaultdict

import threading

from Utils.ulog import log

import time

class BackQueue(object):

    lock = threading.Lock()

    def __init__(self, time_span):
        self.domain_queues = defaultdict(PriorityQueue)
        self.time_stack = dict()
        self.counter = 0
        self.domain_time_span = time_span
        log.info('BACK_QUEUE_TIME_SPAN: {} ms'.format(self.domain_time_span))

    def size(self):
        return self.counter

    def push_one(self, domain, tuple_value):
        if not self.domain_queues.has_key(domain):
            with BackQueue.lock:
                self.time_stack[domain] = time.time() * 1000
            log.debug('time_stack: {}'.format(self.time_stack))
        with BackQueue.lock:
            self.domain_queues[domain].put(tuple_value)
            self.counter += 1
        log.debug('domain: {}'.format(self.domain_queues))

    def pop_one(self, domain):
        if self.domain_queues[domain].empty():
            with BackQueue.lock:
                del self.domain_queues[domain]
                del self.time_stack[domain]
                return None
        else:
            with BackQueue.lock:
                url = self.domain_queues[domain].get()[1]
                self.counter -= 1
                self.time_stack[domain] = time.time() * 1000
                return url

    def push_out(self):
        if len(self.time_stack) == 0:
            log.info('NO URL in BACK QUEUE, sleep {} seconds'.format(1))
            time.sleep(1)
        current_ms = time.time() * 1000
        for domain in self.time_stack.keys()[:]:
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
