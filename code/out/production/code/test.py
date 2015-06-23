#
# # import struct
#
#
# # output = open('./test', 'wb')
# # num = [12, 14, 15, 16]
# #
# # b2 = struct.pack('4H', *num)
# #
# # print 'b2.len: {}'.format(len(b2))
# #
# # b3 = struct.unpack('Ibh', b2[13:20])
# #
# # b3 = struct.unpack_from('I', b2, 13)
# #
# # print b3
# #
# # output.write(b2)
# # print output.tell()
# # output.close()
#
#
# # fmt = ''.join(['I', 'H'])
# #
# # print fmt
# #
# # num1 = 1769824134
# # num2 = 123
# # b2 = struct.pack(fmt, num1, num2)
# # output.write(b2)
# # print output.tell()
# # output.close()
#
#
# from Index.CacheReader import CacheReader
# # input_file = open('./Index/IndexFile/2.index', 'rb')
# # # 3IIBHIBH
# # input_file.seek(160)
# # b = input_file.read(24)
# # print input_file.tell()
# # num2 = struct.unpack('6I', b)
# # print struct.calcsize('3IIIIIII3IIIIIIIII3IIIIIIIII3IIIIIII3IIII3IIII3IIII3IIII3IIII3IIII')
# # print struct.calcsize('3IIB')
# # print struct.calcsize('H')
# # print num2
#
# # d = CacheReader(num2).read_all()
# # for token in d:
# #     print token, ': ', d[token]
#
#
#
#
#
# #
# # input_file.seek(4)
# # b = input_file.read()
# #
# # seq = struct.unpack('I', b)
# # print(seq)
#
# # a='hello'
# #
# # b='world!'
# #
# # c=2
# #
# # d=45.123
# #
# # bytes=struct.pack('5s6sif',a,b,c,d)
# #
# #
# # a1,b1,c1,d1=struct.unpack('5s6sif',bytes)
# #
# # print a1, b1, c1, d1
# #
# # num = [4294967295,14,15,16,17]
# #
# # b2 = struct.pack('5I', *num)
# #
# # ba = bytearray(b2)
# #
# # print struct.unpack('I', ba[0:4])
#
# #
# # import collections
# #
# # d = {'a':(0,3), 'b':(3,1), 'c':(4, 4)}
# #
# # dd = dict()
# # for k in d:
# #     dd[k] = d[k][1]
# #
# # dd = collections.Counter(dd)
# # for k,v in dd.most_common(len(dd)):
# #     print k, v
#
# #
# # for i in range(0, 100):
# #     print struct.calcsize('{}s'.format(i))
#
#
# # import array
#
# # a = array.array('H', xrange(10))
# # print a.buffer_info()
# # print a.buffer_info()[1] * a.itemsize
#
#
# # b = array.array('I', xrange(10))
# #
# # a.extend(b)
#
#
#
# # print len(bytearray(a))
#
# # a.byteswap()
#
#
#
# # def vb_encode(number):
# #     bytes = []
# #     while True:
# #         bytes.insert(0, number % 128)
# #         if number < 128:
# #             break
# #         number /= 128
# #     bytes[-1] += 128
# #     return pack('%dB' % len(bytes), *bytes)
#
#
# # def vb_encode(number):
# #     bytes = []
# #     while True:
# #         bytes.insert(0, number % 128)
# #         if number < 128:
# #             break
# #         number /= 128
# #     bytes[-1] += 128
# #     return pack('%dB' % len(bytes), *bytes)
#
# #
# # import sys
# #
# # import heapq as queue
# #
# # span = sys.maxint
# # heap = [2, 4, 5, 6, 12, 45, 56]
# # heap.reverse()
# # queue.heapify(heap)
# # while heap:
# #     print queue.heappop(heap)
# #
# # queue.heappop(heap)
# #
# # heads = [None] * 10
# #
# # print heads
#
#
# #
# # from collections import defaultdict
# #
# # d = defaultdict(set)
# #
# # d[1].add(11)
# # d[1].add(12)
# # d[2].add(21)
# # d[3].add(31)
# # d[3].add(32)
# #
# # print d
#
#
# # from HTMLParser import HTMLParser
# #
# # class CleanTextParser(HTMLParser):
# #     '''
# #     use one CleanTextParser for a html.
# #     '''
# #     def __init__(self):
# #         HTMLParser.__init__(self)
# #         self.clean = False
# #         self.clean_this = False
# #         self.lst = []
# #
# #     def handle_starttag(self, tag, attrs):
# #         if tag == 'body':
# #             self.clean = True
# #         if self.clean:
# #             self.clean_this = not (tag == 'link' or tag == 'script' or tag == 'style')
# #
# #     def handle_endtag(self, tag):
# #         pass
# #
# #     def handle_data(self, data):
# #         d = data.strip()
# #         if self.clean_this and d:
# #             self.lst.append(d)
# #
# #     def feed(self, html):
# #         HTMLParser.feed(self, html)
# #         return ' '.join(self.lst)
#
#
# # from bs4 import BeautifulSoup
# # from urlparse import urlparse
# # import robotparser
# # import Queue
# # import urllib2
# # import time
# # import re
# # import sys
# # import mmh3
#
#
# # url = 'http://www.history.com/topics/american-revolution/american-revolution-history'
#
# # page = urllib2.urlopen(url)
# # print page.getcode()
#
# # print type(page.info())
# #
# # print page.info()
#
# # print page.geturl()
#
# # opener = urllib2.build_opener()
# # opener.addheaders = [('User-agent', 'Mozilla/5.0')]
# # response = opener.open(url)
#
# # print response
#
# # print response.info()
#
# # print response.read()
#
# # html = response.read()
#
# # soup = BeautifulSoup(html)
#
# # print soup.find('body').get_text()
#
# # print CleanTextParser().feed(html)
#
#
#
# # l = [1,2,3]
# # try:
# #     del l[-1]
# #     del l[-1]
# #     del l[-1]
# #     del l[-1]
# # except IndexError:
# #     print 'here is the error'
#
#
# # import eventlet
# # import gevent
# # from gevent.pool import Pool
#
# # from Utils.LOG import log
#
# # pool = eventlet.GreenPool()
#
# # pool = Pool(10)
#
#
#
#
# # from multiprocessing import Process
# #
# # def f1():
# #     while True:
# #         # log.info('in f1')
# #         print 'in f1'
# #         time.sleep(1)
# #
# # def f2():
# #     while True:
# #         # log.info('in f2')
# #         print 'in f2'
# #         time.sleep(1)
# #
# # if __name__ == '__main__':
# #     p1 = Process(target=f1)
# #     p2 = Process(target=f2)
# #     p1.start()
# #     p1.join()
# #     p2.start()
# #     p2.join()
# #
# #     # print 'after p1'
# #     print 'after p2'
#
#
#
# # gevent.joinall([pool.spawn(f1), pool.spawn(f2)])
#
#
# # from multiprocessing import Pool
# #
# # def f(x):
# #     return x * x
# #
# # if __name__ == '__main__':
# #     p = Pool(5)
# #     p.join()
# #     print(p.map(f, [1, 2, 3]))
#
# # from threading import Thread
# # import time
# #
# # class Task(Thread):
# #     def __init__(self, msg):
# #         Thread.__init__(self)
# #         self.msg = msg
# #
# #     def run(self):
# #         while True:
# #             print self.msg
# #             time.sleep(1)
# #
# #
# # if __name__ == '__main__':
# #     t1 = Task('in t1')
# #     t2 = Task('in t2')
# #     t1.start()
# #     t2.start()
# #     t1.join()
# #     t2.join()
#
#
# from multiprocessing import Process
#
#
# c=" "
# out=" "
#
# def pi():
#     print ("started")
#     out=" "
#     while 1:
#
#
# def man():
#
#     while(1):
# # loop contents
#
# if __name__ == '__main__':
#
#     p1=Process(target=pi,args=())
#     p2=Process(target=man,args=())
#
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()


# import time
# # from multiprocessing import Process
# from Utils.LOG import log
# from multiprocessing import Pool
#
# def pi():
#     log.info("pi started")
#     while 1:
#         # print 'in pi'
#         time.sleep(1)
#         log.info('in pi')
#
# #  loop contents
#
# def man():
#     log.info("man started")
#     while 1:
#         time.sleep(1)
#         log.info('in man')
# # loop contents
#
# if __name__ == '__main__':
#
#     pool = Pool(10)
#     pool.apply_async(pi)
#     pool.apply_async(man)
#     pool.close()
#     pool.join()

    # pool.join()


    # p1=Process(target=pi,args=())
    # p2=Process(target=man,args=())
    #
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()



from multiprocessing import Pool
from multiprocessing.connection import Listener
from array import array
from multiprocessing.connection import Client
from array import array
import time


def f1():
    address = ('localhost', 9000)     # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey='secret password')

    conn = listener.accept()
    print 'connection accepted from', listener.address
    while True:
        conn.send_bytes('hello')
        time.sleep(1)
    conn.close()
    listener.close()


def f2():
    address = ('localhost', 9000)
    conn = Client(address, authkey='secret password')
    while True:
        print conn.recv_bytes()
    conn.close()

def start():
    pool = Pool(2)
    pool.apply_async(f2)
    pool.apply_async(f1)
    pool.close()
    pool.join()

if __name__ == '__main__':

    from Crawl.MemShareManager import MemShareManager

    from Queue import PriorityQueue

    q = PriorityQueue()

    mgr = MemShareManager()
    mgr.start()

    pr_q1 = mgr.PriorityQueue()

    pr_q1.put((1, '111'))

    print pr_q1.get()

    pr_q2 = mgr.PriorityQueue()



    # start()