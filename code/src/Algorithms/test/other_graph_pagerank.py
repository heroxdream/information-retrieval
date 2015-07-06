__author__ = 'hanxuan'

from Algorithms.PageRank import PageRank

from collections import defaultdict

from Utils.ulog import log

from Algorithms import util_methods

link_file = '/Users/hanxuan/Dropbox/neu/summer15/information retrieval/wt2g_inlinks.txt'

docno_id_map = dict()
id_docno_map = dict()
def build_adjacent_list():

    id_counter = 0

    adjacent_list = defaultdict(list)

    edges = 0

    in_put_file = open(link_file, 'r')
    while True:
        line = in_put_file.readline()

        if line == '': break

        groups = line.split(' ')
        node = groups[0]
        if node not in docno_id_map: id_counter = put_to_maps(id_counter, node)
        if node not in adjacent_list: adjacent_list[docno_id_map[node]] = []

        neighbours = groups[1:]
        for neighbour in neighbours:
            if neighbour not in docno_id_map: id_counter = put_to_maps(id_counter, neighbour)
            adjacent_list[docno_id_map[neighbour]].append(docno_id_map[node])
            edges += 1

    in_put_file.close()
    log.info('adjacent_list size {}|{}'.format(len(adjacent_list), edges))
    return adjacent_list

def put_to_maps(id_counter, url):
    docno_id_map[url] = id_counter
    id_docno_map[id_counter] = url
    id_counter += 1
    return id_counter

def run():

    aj_list = build_adjacent_list()

    pr = PageRank(aj_list)
    pr.loop()
    top_500 = pr.top_results(500)

    craw_pr_file = 'results/other.pagerank.500.txt'
    util_methods.write_to_file(id_docno_map, top_500, craw_pr_file)

if __name__ == '__main__':
    run()

