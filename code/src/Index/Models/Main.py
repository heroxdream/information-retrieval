__author__ = 'hanxuan'

from Index.IndexManager import IndexManager

from Index.Models.OkapiBM25 import OkapiBM25

from Index.Models.OkapiTF import OkapiTF

from Index.Models.LMLaplace import LMLaplace

from Index.Models.BLMLaplace import BLMLaplace

import os.path

import time

from RetrievalModel.LOG import log

query_file_path = "/Users/hanxuan/Dropbox/neu/summer15/information retrieval/data/AP_DATA/query_desc.51-100.short.txt"

def okapi_bm25(index_manager):
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.okapi.bm25'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break
        bm25 = OkapiBM25(current_line, index_manager)

        bm25.term_regulate()

        bm25.score()

        bm25.print_result(output_file)

def okapi_tf(index_manager):
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.okapi.tf'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break

        tf = OkapiTF(current_line, index_manager)

        tf.term_regulate()

        tf.score()

        tf.print_result(output_file)


def lmlapalce(index_manager):
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.lm.laplace'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break

        lml = LMLaplace(current_line, index_manager)

        lml.term_regulate()

        lml.score()

        lml.print_result(output_file)

def bigram(index_manager):
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.bigram.laplace'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break
        bi = BLMLaplace(current_line, index_manager)

        bi.term_regulate()

        bi.score()

        bi.print_result(output_file)

if __name__ == '__main__':

    t1 = time.time()

    im = IndexManager()

    okapi_bm25(im)

    okapi_tf(im)

    lmlapalce(im)

    bigram(im)

    t2 = time.time()

    log.info('\n' + '*' * 50)
    log.info('ModelTest Finished, time time: {} min...'.format((t2 - t1) * 1.0 / 60))
