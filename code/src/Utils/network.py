__author__ = 'hanxuan'
# code: utf-8
import re
from urlparse import urlparse

def get_host(url):
    authority_regex = re.compile('^(?:([^\@]+)\@)?([^\:]+)(?:\:(.+))?$')
    authority = urlparse(url).netloc
    host = authority_regex.match(authority).groups()[1]
    return host
