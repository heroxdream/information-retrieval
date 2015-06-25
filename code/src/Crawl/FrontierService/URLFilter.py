# -*- coding: utf-8 -*-
__author__ = 'hanxuan'

from Utils.ulog import log

from pybloom import ScalableBloomFilter

from threading import RLock

class URLFilter(object):

    lock = RLock()

    def __init__(self):
        self.forbidden_keys = ['video', 'facebook', 'youtube', 'twitter', 'instagram', 'tv',
                               'amazon', 'ebay', 'photo', 'image', 'game', 'shop', 'foursquare']
        self.seen = ScalableBloomFilter(initial_capacity=10000, mode=ScalableBloomFilter.LARGE_SET_GROWTH)

    def forbidden_key_word(self, url):
        for key_word in self.forbidden_keys:
            if key_word in url:
                log.debug('## FORBIDDEN: {}'.format(url))
                return False
        return True

    @staticmethod
    def is_english(url):
        try:
            url.decode('ascii')
        except UnicodeDecodeError:
            log.debug('## NON-ENGLISH PAGE DETECTED: {}'.format(url))
            return False
        else:
            return True

    def pass_check(self, url):
        with URLFilter.lock:
            if url in self.seen:
                log.debug('## SEEN: {}'.format(url))
                return False
            self.seen.add(url)
            return self.forbidden_key_word(url) and self.is_english(url)
