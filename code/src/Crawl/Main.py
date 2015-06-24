__author__ = 'hanxuan'
from Crawl.setup_es_ import create_index, DATA_SET

from Crawler.SpiderConfig import SpiderConfig

from Crawler.Spider import Spider

from FrontierService.Frontier import Frontier

from multiprocessing import Process

from Utils.uredis import rs

from Utils.ues import es


if __name__ == '__main__':

    rs.flushall()

    es.indices.delete(index=DATA_SET, ignore=[400, 404])
    create_index(es)

    config = SpiderConfig()
    config.max_threads = 50
    config.seeds_path = './seeds'
    config.domain_fetch_time_span = 2000
    config.max_tasks = 1000000000

    spider = Spider(config)
    frontier = Frontier(config.domain_fetch_time_span)

    frontier_service = Process(target=frontier.start)
    spider_service = Process(target=spider.start)

    frontier_service.start()
    spider_service.start()
    frontier_service.join()
    spider_service.join()
