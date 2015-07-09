__author__ = 'hanxuan'
from elasticsearch import Elasticsearch

cluster = Elasticsearch([
    # {'host':'169.254.165.29', 'port':9201}
    {'host':'169.254.26.130', 'port':9201}
])