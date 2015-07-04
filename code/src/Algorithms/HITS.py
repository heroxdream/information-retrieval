__author__ = 'hanxuan'

from Utils.ulog import log

class HITS(object):

    MAX_ROUND = 20

    def __init__(self, out_link_map, in_link_map):
        self.out_link_map = out_link_map
        self.in_link_map = in_link_map
        self.nodes = out_link_map.keys()
        self.hub = dict()
        self.authority = dict()
        for i in self.nodes:
            self.hub[i] = 1
            self.authority[i] = 1

    def loop(self):

        round_counter = 0

        while round_counter < HITS.MAX_ROUND:

            log.info('{} ROUND start...'.format(round_counter))

            for node in self.nodes:
                in_links = self.in_link_map[node]
                for link in in_links:
                    self.authority[node] += self.hub[link]

            for node in self.nodes:
                out_links = self.out_link_map[node]
                for link in out_links:
                    self.hub[node] += self.authority[link]

            self.authority = HITS.normalize(self.authority)
            self.hub = HITS.normalize(self.hub)

            round_counter += 1

        log.info('HITS finished...')

    @staticmethod
    def normalize(m):
        nm = dict()
        m_sum = 0
        for node in m: m_sum += pow(m[node], 2)
        m_sum = pow(m_sum, 0.5)
        for node in m: nm[node] = m[node] * 1.0 / m_sum
        return nm
