__author__ = 'hanxuan'

from Utils.ulog import log

from util_methods import top_results, perplexity, kl


import copy

class PageRank(object):

    ALPHA = 0.15
    THRESHOLD = 0.000001
    MAX_ROUND = 50

    def __init__(self, adjacent_list):
        self.adjacent_list = adjacent_list
        self.nodes = sorted(self.adjacent_list.keys())
        self.current_score = [0] * len(self.nodes)
        self.last_score = [0] * len(self.nodes)
        self.result = dict()
        for node in self.nodes: self.last_score[node] = 1
        self.check_index()

    def check_index(self):
        max_idx = max(self.nodes)
        len_nodes = len(self.nodes)
        log.info('node max: {}, node len: {}'.format(max_idx, len_nodes))
        if len_nodes - 1 != max_idx: raise Exception('len_nodes - 1 != max_idx')

    def top_results(self, top_n):
        for i in self.nodes: self.result[i] = self.last_score[i]
        return top_results(self.result, top_n)

    def show_kl(self):
        p = copy.copy(self.current_score)
        q = copy.copy(self.last_score)
        k_l = kl(p, q)
        log.info('kl: {}'.format(k_l))

    def show_perplexity(self):
        p = copy.copy(self.current_score)
        pp = perplexity(p)
        log.info('perplexity: {}'.format(pp))

    def loop(self):

        round_counter = 0

        while True:
            log.info('{} ROUND start...'.format(round_counter))

            for i in self.nodes: self.current_score[i] = PageRank.ALPHA

            log.debug('random access score sum {}'.format(sum(self.current_score)))

            processed_nodes = 0
            bonus_for_all = 0.0
            for node in self.nodes:

                node_score = self.last_score[node]

                if node_score < PageRank.THRESHOLD:
                    bonus_for_all += node_score
                    continue

                out_links = self.adjacent_list[node]
                if len(out_links) > 0:
                    score_for_each = (1.0 - PageRank.ALPHA) * node_score / len(out_links)
                    for out_link in out_links: self.current_score[out_link] += score_for_each
                else:
                    bonus_for_all += node_score

                processed_nodes += 1

            bonus_for_each = bonus_for_all * (1.0 - PageRank.ALPHA) / len(self.nodes)
            log.debug('bonus for each/all : {}/{}'.format(bonus_for_each, bonus_for_all))
            for i in self.nodes: self.current_score[i] += bonus_for_each
            log.info('SCORE: current {} ~ last {} processed node: {}'.
                     format(sum(self.current_score), sum(self.last_score), processed_nodes))

            # self.show_perplexity()
            # self.show_kl()

            tmp = self.last_score
            self.last_score = self.current_score
            self.current_score = tmp
            log.debug('mem address: {} {} {}'.format(id(tmp), id(self.last_score), id(self.current_score)))

            round_counter += 1
            if round_counter == PageRank.MAX_ROUND:
                log.info('PAGERANK finished ...')
                break
