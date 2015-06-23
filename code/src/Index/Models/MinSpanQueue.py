__author__ = 'hanxuan'

import heapq as queue
import sys

from Utils.log import log


class MinSpanQueue(object):
    def __init__(self, q_list):
        self.q_list = q_list
        self.heads = [None] * len(q_list)
        self.search_finished = False
        self.min_idx = -1

        self.heapfy()
        self.init_heads()

    def heapfy(self):
        for heap in self.q_list:
            queue.heapify(heap)

    def init_heads(self):
        for i in range(0, len(self.heads)):
            self.heads[i] = queue.heappop(self.q_list[i])

    def find_min(self):
        idx = -1
        minimum = sys.maxint
        for i in range(0, len(self.heads)):
            if minimum > self.heads[i]:
                minimum = self.heads[i]
                idx = i
        self.min_idx = idx
        return minimum

    def update_min(self):
        if self.q_list[self.min_idx]:
            self.heads[self.min_idx] = queue.heappop(self.q_list[self.min_idx])
        else:
            self.search_finished = True

    def find_max(self):
        maximum = -1
        for i in range(0, len(self.heads)):
            maximum = max(maximum, self.heads[i])
        return maximum

    def span(self):
        maximum = self.find_max()
        minimum = self.find_min()
        self.update_min()
        log.debug('max: {}, min: {}'.format(maximum, minimum))
        return maximum - minimum

    def min_span(self):
        min_span = sys.maxint
        while not self.search_finished:
            min_span = min(min_span, self.span())
            log.debug(self.heads)
        return min_span

if __name__ == '__main__':
    h1 = [4]
    h2 = [7,6,8, 99]
    h3 = [3, 5]
    l = [h1, h2 , h3]
    print l

    msq = MinSpanQueue(l)
    print msq.min_span()
    # print msq.heads

# import random
#
# h1 = random.sample(xrange(100), 10)
#
# h2 = random.sample(xrange(150), 20)
#
# h3 = random.sample(xrange(250), 80)
#
# h4 = random.sample(xrange(200), 60)
#
# h5 = random.sample(xrange(150), 40)
#
# h6 = random.sample(xrange(100), 50)
#
#

