__author__ = 'hanxuan'

from Utils.ulog import log

class PageRank(object):

    ALPHA = 0.15

    MAX_ROUND = 20

    def __init__(self, adjacent_list):
        self.adjacent_list = adjacent_list
        self.nodes = self.adjacent_list.keys()
        self.current_score = dict()
        self.last_score = dict()
        for node in self.nodes: self.last_score[node] = 1

    def loop(self):

        round_counter = 0

        while True:
            log.info('{} ROUND start...'.format(round_counter))

            for i in self.nodes: self.current_score[i] = PageRank.ALPHA

            log.info('random access score sum {}'.format(sum(self.current_score.values())))

            for node in self.nodes:

                node_score = self.last_score[node]

                out_links = self.adjacent_list[node]

                if len(out_links) > 0:
                    score_for_each = (1.0 - PageRank.ALPHA) * node_score / len(out_links)
                    for out_link in out_links:
                        self.current_score[out_link] += score_for_each
                else:
                    for each in self.nodes: self.current_score[each] += (1.0 - PageRank.ALPHA) * node_score / len(self.nodes)

            log.info('SCORE: current {} ~ last {}'.format(sum(self.current_score.values()), sum(self.last_score.values())))

            self.last_score = self.current_score
            self.current_score = dict()

            round_counter += 1
            if round_counter == PageRank.MAX_ROUND:
                log.info('PAGERANK finished ...')
                break

