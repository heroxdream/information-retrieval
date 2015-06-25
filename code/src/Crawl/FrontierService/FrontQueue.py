__author__ = 'hanxuan'

from Queue import Queue

from collections import defaultdict

import multiprocessing as mp

from Utils.ulog import log

import time

import math

import random

class FrontQueue(object):

    LEVEL_HIGH = 1
    LEVEL_LOW = 7
    IN_LINK_MAX = 1000

    def __init__(self):
        self.level_queue = defaultdict(Queue)
        self.key_words = ['history', 'america', 'wikipedia', 'revolution', 'war', 'independe']
        self._size = 0
        self.lock = mp.Lock()

    def size(self):
        return self._size

    def push(self, level, url):
        with self.lock:
            self._size += 1
            self.level_queue[level].put(url)

    def pop(self, level):
        with self.lock:
            self._size -= 1
            return self.level_queue[level].get()

    def push_one(self, url):
        level = self.level_calc(url)
        self.push(level, url)

    def pop_one(self):
        if self.size() == 0:
            log.info('NO url in FRONT_QUEUE, sleep 1 s')
            time.sleep(1)
            return None

        keys = sorted(self.level_queue.keys(), key=lambda *args: random.random())
        for level in keys:
            if not self.level_queue[level].empty():
                url = self.pop(level)
                log.debug('************** return {} {}'.format(level, url))
                return level, url

    def level_calc(self, url):
        level = FrontQueue.LEVEL_LOW * 1.0
        for key_word in self.key_words:
            if key_word in url.lower():
                level = max(FrontQueue.LEVEL_HIGH, level - 0.2)
        log.debug('********************** level: {}'.format(level))
        return math.floor(level)


if __name__ == '__main__':
    # f = FrontQueue()
    # f.push_one('history')
    # f.push_one('can')
    # print f.content_size
    #
    # print f.pop_one()
    # print f.content_size
    # print f.pop_one()
    # print f.content_size
    # print f.pop_one()
    # print f.pop_one()

    a = [1, 2, 3, 4, 5, 6, 7, 100, 19999999999]

    def f(count):
        count = min(FrontQueue.IN_LINK_MAX, count)
        print FrontQueue.LEVEL_LOW - 1 - (count - FrontQueue.LEVEL_HIGH) * 5.0 / (FrontQueue.IN_LINK_MAX - FrontQueue.LEVEL_HIGH)
    map(f, a)




