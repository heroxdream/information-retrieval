__author__ = 'hanxuan'

from Utils.ulog import log

from multiprocessing.connection import Listener

from multiprocessing.connection import Client

from multiprocessing import Process

from Crawl.MemShareManager import MemShareManager

from Utils.network import get_host


class Frontier(object):

    PULL_IN_PORT = 9000
    PUSH_OUT_PORT = 9001

    def __init__(self, time_span):
        log.info('********** FRONTIER STARTED **********')
        mgr = MemShareManager()
        mgr.start()
        self.front_queue = mgr.FrontQueue()
        self.back_queue = mgr.BackQueue(time_span)
        self.filter = mgr.URLFilter()
        self.authkey = 'han.xuan'

    def start(self):
        p1 = Process(target=self.pull_in)
        p2 = Process(target=self.front_to_back_process)
        p3 = Process(target=self.push_out)
        # p4 = Process(target=self.simu)
        p1.start(); p2.start(); p3.start();
        # p4.start()
        p1.join(); p2.join(); p3.join();
        # p4.join()

    def pull_in(self):
        address = ('127.0.0.1', Frontier.PULL_IN_PORT)
        listener = Listener(address, authkey=self.authkey)
        connection = listener.accept()
        log.info('Frontier : connection accepted from {}'.format(listener.address))
        while True:
            url = connection.recv_bytes()
            log.debug('url pull in: {}'.format(url))
            if self.filter.pass_check(url):
                self.front_queue.push_one(url)
                log.debug('pass_check: {}'.format(url))
        connection.close()
        listener.close()

    def front_to_back_process(self):
        while True:
            level_url = self.front_queue.pop_one()
            if level_url:
                level, url = level_url
                domain = get_host(url)
                self.back_queue.push_one(domain, (level, url))
                log.debug('F2B: level:{}, url:{}'.format(level, url))

    def push_out(self):
        address = ('127.0.0.1', Frontier.PUSH_OUT_PORT)
        connection = Client(address, authkey=self.authkey)
        log.info('Frontier : connection established from {}'.format(address))
        while True:
            url = self.back_queue.push_out()
            if url:
                connection.send_bytes(url)
                log.debug('FRONTIER PUSH OUT: {}'.format(url))
        connection.close()

    # def randomword1(self, len):
    #     return ''.join(random.choice(string.lowercase) for i in range(len))
    #
    # def randomword2(self, len):
    #     return ''.join(random.choice(string.octdigits) for i in range(len))
    #
    # def simu(self):
    #     log.info('in simu')
    #
    #     address = ('127.0.0.1', Frontier.PUSH_OUT_PORT)
    #     listener = Listener(address, authkey=self.authkey)
    #     connection1 = listener.accept()
    #
    #     address = ('127.0.0.1', Frontier.PULL_IN_PORT)
    #     connection = Client(address, authkey=self.authkey)
    #     while True:
    #         url = 'http://' + self.randomword1(10)
    #         connection.send_bytes(url)
    #         log.info('simu created: {}'.format(url))
    #         time.sleep(10)
    #     connection.close()


if __name__ == '__main__':
    Frontier(1000).start()

    # print Frontier.get_host('http://play.facebook.com')