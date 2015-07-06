__author__ = 'hanxuan'

from util_methods import top_results

from Utils.ulog import log

class SALSA(object):

    MAX_ROUND = 20

    def __init__(self, out_link_map, in_link_map):
        self.out_link_map = out_link_map
        self.in_link_map = in_link_map
        self.nodes = out_link_map.keys()
        self.hub = dict()
        self.authority = dict()
        for i in self.nodes:
            if len(out_link_map[i]) > 0: self.hub[i] = 1
            if len(in_link_map[i]) > 0: self.authority[i] = 1

    def top_hub(self, top_n):
        return top_results(self.hub, top_n)

    def top_authority(self, top_n):
        return top_results(self.authority, top_n)

    def loop(self):
        counter = 0
        while counter < SALSA.MAX_ROUND:

            log.info('SALSA round: {}'.format(counter))

            counter += 1
            self.loop_hub()
            self.loop_authority()

        log.info('SALSA finished...')

    def _loop_hub(self):
        hub_tmp = dict()
        for node in self.hub.iterkeys():
            hub_score_for_this_node = 0.0
            authorities = self.out_link_map[node]
            for authority in authorities:
                hubs = self.in_link_map[authority]
                in_size = len(hubs)
                for hub in hubs:
                    if hub == node: continue
                    out_size = len(self.out_link_map[hub])
                    hub_score = self.hub[hub]
                    hub_score_for_this_node += hub_score * 1.0 / in_size / out_size

            hub_tmp[node] = hub_score_for_this_node

        self.hub = hub_tmp

    def loop_hub(self):

        hub_tmp = dict()

        authority_score = dict()

        for authority in self.authority.iterkeys():
            hubs = self.in_link_map[authority]
            a_score = 0.0
            for hub in hubs:
                a_score += self.hub[hub] * 1.0 / len(self.out_link_map[hub])
            authority_score[authority] = a_score

        for hub in self.hub.iterkeys():
            authorities = self.out_link_map[hub]
            h_score = 0.0
            for authority in authorities:
                h_score += (authority_score[authority] - self.hub[hub] * 1.0 / len(self.out_link_map[hub])) / len(self.in_link_map[authority])
            hub_tmp[hub] = h_score

        self.hub = hub_tmp

    def obselete_loop_authority(self):
        authority_tmp = dict()
        for node in self.authority.iterkeys():
            authority_score_for_this_node = 0.0
            hubs = self.in_link_map[node]
            for hub in hubs:
                authorities = self.out_link_map[hub]
                out_size = len(authorities)
                for authority in authorities:
                    if authority == node: continue
                    in_size = len(self.in_link_map[authority])
                    authority_score = self.authority[authority]
                    authority_score_for_this_node += authority_score * 1.0 / in_size / out_size

            authority_tmp[node] = authority_score_for_this_node

        self.authority = authority_tmp

    def loop_authority(self):

        authority_tmp = dict()

        hub_score = dict()

        for hub in self.hub.iterkeys():
            authorities = self.out_link_map[hub]
            h_score = 0.0
            for authority in authorities:
                h_score += self.authority[authority] * 1.0 / len(self.in_link_map[authority])
            hub_score[hub] = h_score

        for authority in self.authority.iterkeys():
            hubs = self.in_link_map[authority]
            a_score = 0.0
            for hub in hubs:
                a_score += (hub_score[hub] - self.authority[authority] * 1.0 / len(self.in_link_map[authority])) / len(self.out_link_map[hub])
            authority_tmp[authority] = a_score

        self.authority = authority_tmp


