__author__ = 'hanxuan'

from Utils.ulog import log

from pybloom import ScalableBloomFilter

import mmh3

class URLFilter(object):
    def __init__(self):
        self.forbidden_keys = ['video', 'facebook', 'youtube', 'twitter', 'instagram', 'tv',
                               'amazon', 'ebay', 'photo', 'image', 'game', 'shop']
        self.seen = ScalableBloomFilter(initial_capacity=10000, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        # self.seen = set()

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
        hash_code = mmh3.hash64(url)
        if hash_code in self.seen:
            log.debug('## SEEN: {}'.format(url))
            return False
        self.seen.add(hash_code)
        return self.forbidden_key_word(url) and self.is_english(url)
