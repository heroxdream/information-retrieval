__author__ = 'hanxuan'

from Crawl.FrontierService.Frontier import Frontier

from multiprocessing import Queue

from multiprocessing.connection import Client

from multiprocessing.connection import Listener

from multiprocessing import Process

from multiprocessing import Manager

import multiprocessing

from Utils.ulog import log

from Utils.ues import es

from Crawl.setup_es_ import create_index, DATA_SET

# from SpiderConfig import SpiderConfig

import time

import urllib2

from lxml import etree

from Parser import ParserTarget

import robotparser

from Utils.network import get_host

from Utils.uredis import rs


class Spider(object):

    lock = multiprocessing.Lock()

    PUSH_OUT_PORT = Frontier.PULL_IN_PORT
    PULL_IN_PORT = Frontier.PUSH_OUT_PORT

    def __init__(self, cfg):
        mgr = Manager()
        self.config = cfg
        self.url_queue = Queue()
        self.robots = mgr.dict()
        self.authkey = 'han.xuan'
        self.load_seeds()
        self.max_threads = mgr.Value('l', self.config.max_threads)
        self.max_tasks = mgr.Value('l', self.config.max_tasks)
        self.process_count = mgr.Value('l', 0)
        self.finished_page = mgr.Value('l', 0)
        self.error_page = mgr.Value('l', 0)

    def start(self):
        p1 = Process(target=self.crawl)
        p2 = Process(target=self.push_out)
        p1.start()
        p2.start()
        p1.join()
        p2.join()

    def load_seeds(self):
        seeds_path = self.config.seeds_path
        seeds_file = open(seeds_path, 'r')
        while True:
            seed_url = seeds_file.readline().strip()
            if seed_url == '':
                break
            self.url_queue.put(seed_url)
        seeds_file.close()

    def pop_one(self):
        if self.url_queue.empty():
            log.info('NO URL in SPIDER QUEUE, sleep 1 second ...')
            time.sleep(1)
            return None
        else:
            return self.url_queue.get()

    def push_out(self):
        address = ('127.0.0.1', Spider.PUSH_OUT_PORT)
        connection = Client(address, authkey=self.authkey)
        log.info('Spider : connection established from {}'.format(address))
        while True:
            log.debug('in spider push_out')
            url = self.pop_one()
            if url:
                try:
                    connection.send_bytes(url)
                    log.debug('SPIDER PUSH : {}'.format(url))
                except Exception,e:
                    log.debug('Exception {}'.format(e))
        connection.close()

    def crawl(self):
        address = ('127.0.0.1', Spider.PULL_IN_PORT)
        listener = Listener(address, authkey=self.authkey)
        connection = listener.accept()
        log.info('Spider : connection accepted from {}'.format(address))

        process_pool = []
        while True:
            if Spider.finished_page.value > self.max_tasks.value:
                log.info("############ ALL TASK DONE #############")
                for p in process_pool:
                    if not p.is_alive():
                        log.debug('process not alive')
                        p.terminate()
                        process_pool.remove(p)
                        with Spider.lock: self.process_count.value -= 1
                time.sleep(1000)
                continue

            if self.process_count.value > self.max_threads.value:
                log.info('############# Process Pool is full now, sleep {} seconds #############'.format(1))
                for p in process_pool:
                    if not p.is_alive():
                        log.debug('process not alive')
                        p.terminate()
                        process_pool.remove(p)
                        with Spider.lock: self.process_count.value -= 1
                time.sleep(1)
                continue
            url = connection.recv_bytes()
            p = Process(target=self.task, args=(url,))
            p.daemon = True
            process_pool.append(p)
            p.start()
            with Spider.lock: self.process_count.value += 1
        connection.close()
        listener.close()

    def task(self, url):
        log.debug('*********************** in task: {} ***********************'.format(url))

        domain = get_host(url)
        if domain not in self.robots and 'html' not in domain and 'htm' not in domain and ('com' in domain or 'org' in domain):
            try:
                rp = robotparser.RobotFileParser()
                rp.set_url('http://' + domain + '/robots.txt')
                rp.read()
                log.debug('~~~~~~~~~~~~~~~~~~~ ROBOTS {}~~~~~~~~~~~~~~~~~~~'.format(domain))
                self.robots[domain] = rp
            except Exception, e:
                log.debug('~~~~~~~~~~~~~~~~~~~ FAIL ROBOTS {}~~~~~~~~~~~~~~~~~~~'.format(domain))
                log.debug(e)
        else:
            if domain in self.robots and (not self.robots[domain].can_fetch('*', url)):
                return None

        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            response = opener.open(url)
            header = response.info()
            if 'content-language' in header:
                if 'en' not in header['content-language']:
                    log.debug('NOT english-based page: {}'.format(url))
                    return
            if 'content-type' in header:
                if 'text' not in header['content-type']:
                    log.debug('NOT text-based page: {}'.format(url))
                    return

            log.debug('code: {}'.format(response.getcode()))
            html = str(response.read())
            parser = etree.HTMLParser(encoding='utf-8', target = ParserTarget(url), remove_blank_text=True, remove_comments=True)
            etree.HTML(html, parser)
            text = ' '.join(parser.target.text_lines)
            title = parser.target.title
            links = parser.target.links
            for link in links:
                self.url_queue.put(link)
                rs.incr(link)

            doc = dict(url=url, html=html, header=str(header), text=text, title=title, out_links=links)
            res = es.index(index=DATA_SET, doc_type='document', id=self.finished_page.value, body=doc, timeout=60)
            if res['created']:
                with Spider.lock: self.finished_page.value += 1
                log.info('*********************** task{} finished: {} ***********************'.format(self.finished_page.value, title))
            return url
        except Exception, e:
            with Spider.lock: self.error_page.value += 1
            log.info('ERROR{} ~ URL: {}'.format(self.error_page.value, url))
            log.info('ERROR MSG: {}'.format(e))
        finally:
            opener.close()
            return None

