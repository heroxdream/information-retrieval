# -*- coding: utf-8 -*-
__author__ = 'hanxuan'

from Crawl.FrontierService.Frontier import Frontier

from multiprocessing.connection import Client

from multiprocessing.connection import Listener

from multiprocessing import Process

from multiprocessing import Manager

from Utils.ulog import log

# from Utils.ues import es
# from Crawl.setup_es_ import DATA_SET

from Utils.ucluster import cluster

from Crawl.setup_cluster import DATA_SET

import time

import urllib2

from lxml import etree

from Parser import ParserTarget

import robotparser

from Utils.network import get_host

from Utils.uredis import rs

import threading

from simhash import SimhashIndex, Simhash

import mmh3

import string


class Spider(object):
    lock = threading.Lock()

    PUSH_OUT_PORT = Frontier.PULL_IN_PORT
    PULL_IN_PORT = Frontier.PUSH_OUT_PORT

    def __init__(self, cfg):
        log.info('>>>>>>>>>>> SPIDER STARTED <<<<<<<<<<<')
        mgr = Manager()
        self.config = cfg
        self.url_queue_out = mgr.Queue()
        self.url_queue_in = mgr.Queue()
        self.html_queue = mgr.Queue()
        self.robots = mgr.dict()
        self.authkey = 'han.xuan'
        self.load_seeds()
        self.max_threads = mgr.Value('l', self.config.max_threads)
        self.max_tasks = mgr.Value('l', self.config.max_tasks)
        self.finished_page = mgr.Value('l', 0)
        self.error_page = mgr.Value('l', 0)
        self.finished_store = mgr.Value('l', 0)
        self.error_store = mgr.Value('l', 0)

    def start(self):
        crawl_process = Process(target=self.crawl)
        parse_process = Process(target=self.parse_task)
        pull_in_process = Process(target=self.pull_in)
        push_out_process = Process(target=self.push_out)
        crawl_process.start()
        pull_in_process.start()
        push_out_process.start()
        parse_process.start()
        crawl_process.join()
        pull_in_process.join()
        push_out_process.join()
        parse_process.join()

    def load_seeds(self):
        seeds_path = self.config.seeds_path
        seeds_file = open(seeds_path, 'r')
        while True:
            seed_url = seeds_file.readline().strip()
            if seed_url == '':
                break
            self.url_queue_out.put(seed_url)
        seeds_file.close()
        log.debug('seeds loaded...')

    def pop_one(self):
        if self.url_queue_out.empty():
            log.info('NO URL in SPIDER QUEUE, sleep 1 second ...')
            time.sleep(1)
            return None
        else:
            return self.url_queue_out.get()

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
                except Exception, e:
                    log.warning('Spider PUSH OUT ERROR: {}'.format(e))
                    continue
        connection.close()

    def pull_in(self):
        address = ('127.0.0.1', Spider.PULL_IN_PORT)
        listener = Listener(address, authkey=self.authkey)
        connection = listener.accept()
        log.info('Spider : connection accepted from {}'.format(address))

        while True:
            try:
                url = connection.recv_bytes()
                self.url_queue_in.put(url)
            except Exception, e:
                log.warning('Spider PULL IN ERROR: {}'.format(e))
                continue
        connection.close()
        listener.close()

    def crawl(self):
        process_pool = set()
        while True:
            if self.finished_store.value > self.max_tasks.value:
                log.info("############ ALL TASK DONE #############")
                for p in process_pool:
                    if not p.is_alive():
                        log.debug('process not alive')
                        p.terminate()
                        process_pool.remove(p)
                time.sleep(1000)
                continue

            if len(process_pool) > self.max_threads.value:
                log.info('POOL({}/{}) is full now'.
                         format(len(process_pool), self.max_threads.value))
                for p in process_pool.copy():
                    if not p.is_alive():
                        log.debug('process not alive')
                        p.terminate()
                        process_pool.remove(p)
                time.sleep(0.5)
                continue

            if self.url_queue_in.empty():
                log.info('NO URL in CRAWL QUEUE, sleep 1 second ...')
                time.sleep(1)
                continue
            url = self.url_queue_in.get()
            p = Process(target=self.spider_task, args=(url,))
            p.daemon = True

            with Spider.lock: process_pool.add(p)
            p.start()
            p.join(0.1)

    def spider_task(self, url):
        log.debug('IN task: {}'.format(url))

        try:
            domain = get_host(url)
        except Exception, e:
            log.warning('DOMAIN PARSE exception: {}'.format(e))

        if domain not in self.robots:
            try:
                rp = robotparser.RobotFileParser()
                rp.set_url('http://' + domain + '/robots.txt')
                rp.read()
                log.debug('ROBOTS SUCCESS{} {}'.format(len(self.robots), domain))
                with Spider.lock:
                    self.robots[domain] = rp
            except Exception, e:
                log.debug('ROBOTS FAIL {}'.format(domain))
                log.debug(e)
        else:
            if domain in self.robots and (not self.robots[domain].can_fetch('*', url)):
                log.info('FORBIDDEN BY ROBOTS {}'.format(url))
                return None

        try:

            try:
                response = urllib2.urlopen(url, timeout=5)
            except Exception, e:
                log.warning('URLOPEN exception: {}\t{}'.format(url, e))
                return None

            try:

                code = int(response.getcode())
                log.debug('code: {}'.format(response.getcode()))

                if code != 200:
                    return None
                header = response.info()
                if not header:
                    header = dict()
                if 'content-language' in header:
                    if 'en' not in header['content-language']:
                        log.debug('NOT english-based page: {}'.format(url))
                        return
                if 'content-type' in header:
                    if 'text' not in header['content-type']:
                        log.debug('NOT text-based page: {}'.format(url))
                        return
            except Exception, e:
                log.warning('CODE/HEADER exception: {}'.format(e))

            try:
                html = response.read()
                log.debug('HTML encode {}'.format(type(html)))
            except Exception, e:
                with Spider.lock: self.error_page.value += 1
                log.info('HTML READ exception: {}'.format(e))
                return None

            try:
                tpl = url, str(header), html
                self.html_queue.put(tpl)
            except Exception,e:
                log.warning('PUT HTML_QUEUE exception: {}'.format(e))

            with Spider.lock: self.finished_page.value += 1
            log.info('DONE SPIDER TASK {}/{}: {}'.
                     format(self.finished_page.value, self.url_queue_in.qsize(), url))
            return url
        except Exception, e:
            with Spider.lock:
                self.error_page.value += 1
            log.info('ERROR{} ~ URL: {}'.format(self.error_page.value, url))
            log.info('ERROR MSG: {}'.format(e))
        finally:
            return None

    def parse_task(self):

        smh_index = SimhashIndex([], k=3)
        sh_counter = 0
        sh_id = 0

        while True:
            if self.html_queue.empty():
                log.info('EMPTY html_queue, sleep 1 seconds ...')
                time.sleep(10)
                continue

            url, header, html = self.html_queue.get()
            try:
                html = html.decode('utf-8','ignore')
            except Exception,e:
                log.info('HTML decode exception'.format(e))
                return None

            text = ''
            title = ''
            links = []

            try:
                parser = etree.HTMLParser(target=ParserTarget(url), remove_blank_text=True, remove_comments=True)
                etree.HTML(html, parser)
                text = ' '.join(parser.target.text_lines)
                title = parser.target.title
                links = parser.target.links
            except Exception, e:
                log.warning('PARSER exception: {}'.format(e))

            try:
                sm = Simhash(text)
                if smh_index.get_near_dups(sm):
                    sh_counter += 1
                    smh_index.add(str(sh_id), sm)  # very important step to do.
                    sh_id += 1
                    log.info('DUPLICATE {} DETECTED FOR: {} / {}'.format(sh_counter, title, url))
                    continue
                smh_index.add(str(sh_id), sm)  # very important step to do.
                sh_id += 1
            except Exception, e:
                log.warning('SIMHASH exception: {}'.format(e))

            for link in links:
                try:
                    self.url_queue_out.put(link)
                except Exception, e:
                    log.info('URL_QUEUE_OUTPUT exception: {}'.format(e))
                try:
                    rs.incr(link)
                except Exception, e:
                    log.warning('REDIS exception: {}'.format(e))

            try:
                # doc = dict(url=url, html=html, header=header, text=text, title=title, out_links=links)
                # res = es.index(index=DATA_SET, doc_type='document', id=self.finished_store.value, body=doc, timeout=60)
                # if res['created']:
                #     with Spider.lock: self.finished_store.value += 1
                #     log.info('DONE PARSER TASK {}/{} ~ {}'.
                #              format(self.finished_store.value, self.html_queue.qsize(), self.error_store.value))

                url = string.strip(url, '/')
                id_hash = mmh3.hash(url)

                if cluster.exists(index=DATA_SET, id=id_hash):
                    log.info('CLUSTER EXISTS: {}'.format(url))
                    continue

                doc = dict(docno=url, html_Source=html, HTTPheader=header, author='xuan', text=text, title=title, out_links=links)
                res = cluster.index(index=DATA_SET, doc_type='document', id=id_hash, body=doc, timeout=60)
                if res['created']:
                    with Spider.lock: self.finished_store.value += 1
                    log.info('DONE PARSER TASK {}/{} ~ {}'.
                             format(self.finished_store.value, self.html_queue.qsize(), self.error_store.value))
            except Exception, e:
                with Spider.lock:
                    self.error_store.value += 1
                log.warning('ES exception: {}'.format(e))
