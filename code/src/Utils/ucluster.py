__author__ = 'hanxuan'
from elasticsearch import Elasticsearch

cluster = Elasticsearch([
    # {'host':'169.254.165.29', 'port':9201}
    {'host':'172.20.10.2', 'port':9201}
])