__author__ = 'hanxuan'
from elasticsearch import Elasticsearch

cluster = Elasticsearch([
    {'host':'169.254.90.84', 'port':9201}
])
