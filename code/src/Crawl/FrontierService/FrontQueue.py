__author__ = 'hanxuan'

from Queue import Queue

from collections import defaultdict

import threading

from Utils.ulog import log

import time

import math

class FrontQueue(object):

    lock = threading.Lock()

    LEVEL_HIGH = 1
    LEVEL_LOW = 7
    IN_LINK_MAX = 1000

    def __init__(self):
        self.level_queue = defaultdict(Queue)
        self.key_words = ['history', 'america', 'wikipedia', 'revolution', 'war', 'independe']
        self.content_size = 0

    def size(self):
        return self.content_size

    def push_one(self, url):
        level = self.level(url)
        with FrontQueue.lock:
            self.level_queue[level].put(url)
            self.content_size += 1

    def pop_one(self):
        if self.size() == 0:
            log.info('NO url in FRONT_QUEUE, sleep 1 s')
            time.sleep(1)

        with FrontQueue.lock:
            for level in xrange(FrontQueue.LEVEL_HIGH, FrontQueue.LEVEL_LOW + 1):
                if not self.level_queue[level].empty():
                    self.content_size -= 1
                    return level, self.level_queue[level].get()

    def level(self, url):
        level = FrontQueue.LEVEL_LOW * 1.0
        for key_word in self.key_words:
            if key_word in url.lower():
                level = max(FrontQueue.LEVEL_HIGH, level - 0.3)
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




