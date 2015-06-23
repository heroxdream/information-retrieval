__author__ = 'hanxuan'

from multiprocessing.managers import BaseManager
from multiprocessing.managers import DictProxy
from collections import defaultdict
from Queue import PriorityQueue
from FrontierService.BackQueue import BackQueue
from FrontierService.FrontQueue import FrontQueue
from FrontierService.URLFilter import URLFilter
from pybloom import ScalableBloomFilter
from Queue import Queue

class MemShareManager(BaseManager):
    pass

MemShareManager.register('defaultdict', defaultdict, DictProxy)
MemShareManager.register('dict', dict, DictProxy)
MemShareManager.register("PriorityQueue", PriorityQueue)
MemShareManager.register('BackQueue', BackQueue)
MemShareManager.register('URLFilter', URLFilter)
MemShareManager.register('FrontQueue', FrontQueue)
MemShareManager.register('ScalableBloomFilter', ScalableBloomFilter)
MemShareManager.register('Queue', Queue)
# MemShareManager.register('list', list)

