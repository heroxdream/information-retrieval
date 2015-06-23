__author__ = 'Xuan Han'

# import pickle
import pprint
import time
import cPickle

from Constants import DATA_SET
from Utils.ues import es


def term_trim(term):
    term_str = str(term)
    return term_str.split('\'')[1]


def store_term_vector(client):
    print("TermVector stat_dat")
    stat_dat = dict()
    counter = 0
    for doc_id in range(0, 84678, 1):
        counter += 1
        if 0 == counter % 1000:
            print('%s \t documents processed...' % counter)
        result_tv = client.termvector(
            index=DATA_SET,
            doc_type='document',
            id=doc_id,
            fields=['text'],
            body={
                "offsets": False,
                "payloads": False,
                "positions": False,
                "term_statistics": False,
                "field_statistics": False
            }
        )
        # pprint.pprint(result_tv['term_vectors'])
        if len(result_tv['term_vectors']) == 0:
            print(result_tv['term_vectors'], 'NONE')
            stat_dat[doc_id] = 0
            continue
        else:
            terms_stats = result_tv['term_vectors']['text']['terms']
            # print (terms_stats)
            # print(len(terms_stats))
            count = 0
            for term in terms_stats:
                count += terms_stats[term]['term_freq']
            stat_dat[doc_id] = count

    print(stat_dat)

    output = open('doc_len.cpkl', 'wb', 1024 * 1024)
    cPickle.dump(stat_dat, output, protocol=cPickle.HIGHEST_PROTOCOL)
    output.close()
    doc_len_file = open('doc_len.cpkl', 'rb', 1024 * 1024)
    data = cPickle.load(doc_len_file)
    doc_len_file.close()
    print('data from disk:')
    pprint.pprint(data)


def store_stat_info_batch(client):
    term_freq = dict()
    docs_freq = dict()
    doc_length = dict()

    gap = 100
    doc_count = 84678
    counter = 0
    for id_start in range(0, doc_count, gap):
        id_list = []

        for doc_id in range(id_start, min(id_start + gap, doc_count), 1):
            id_list.append(str(doc_id))
            counter += 1
            if counter % 50 == 0:
                print('(%s)/(%s) \t documents processed...' % (counter, doc_count))

        batch_result_tv = client.mtermvectors(
            index=DATA_SET,
            doc_type='document',
            ids=id_list,
            params={
                "tokens": False,
                "term_statistics": False
            }
        )

        for doc in batch_result_tv['docs']:

            # <editor-fold desc="debug of dicts">
            # print('*' * 100)
            # print(docs_freq)
            # print('-' * 100)
            # print(term_freq)
            # print('-' * 100)
            # print(doc_length)
            # print('*' * 100)
            # </editor-fold>

            current_id = doc['_id']
            if len(doc['term_vectors']) == 0:
                print(doc['term_vectors'], 'NONE')
                doc_length[current_id] = 0
                continue
            else:
                terms_stats = doc['term_vectors']['text']['terms']
                count = 0
                for term in terms_stats:
                    term_str = str(term)
                    term_tf_now = terms_stats[term]['term_freq']
                    count += term_tf_now
                    docs_freq[term_str] = terms_stats[term]['doc_freq']
                    if term_freq.has_key(term_str):
                        tf = term_freq[term_str]
                        tf[str(current_id)] = term_tf_now
                        term_freq[term_str] = tf
                    else:
                        term_freq[term_str] = {str(current_id): term_tf_now}

                doc_length[str(current_id)] = count

    output1 = open('Data/doc_length.cpkl', 'wb', 1024 * 1024 * 32)
    cPickle.dump(doc_length, output1, protocol=cPickle.HIGHEST_PROTOCOL)
    # pickle.dump(doc_length, output1)
    output1.close()

    output2 = open('Data/term_freq.cpkl', 'wb', 1024 * 1024 * 32)
    cPickle.dump(term_freq, output2, protocol=cPickle.HIGHEST_PROTOCOL)
    # pickle.dump(term_freq, output2)
    output2.close()

    output3 = open('Data/docs_freq.cpkl', 'wb', 1024 * 1024 * 32)
    cPickle.dump(docs_freq, output3, protocol=cPickle.HIGHEST_PROTOCOL)
    # pickle.dump(docs_freq, output3)
    output3.close()


if __name__ == '__main__':

    t1 = time.time()
    store_stat_info_batch(es)
    t2 = time.time()
    print('Procedure finished, total time:', (t2 - t1) / 60, ' mins...')
