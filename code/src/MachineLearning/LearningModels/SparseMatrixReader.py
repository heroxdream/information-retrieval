__author__ = 'hanxuan'

import numpy as np
from scipy.sparse import csr_matrix

class SparseMatrixReader(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.feature_matrix = None
        self.labels = None
        self.read_text()

    def read_text(self):
        in_file = open(self.file_path, 'r', 1024 * 1024 * 32)
        labels = []
        pointer = 0
        data = []
        indices = []
        idxptr = [pointer]
        while True:
            line = in_file.readline()
            if line == '': break
            elements = line.split()
            labels.append(elements[0])
            features_one_line = elements[1:]
            for idx_feature_pair in features_one_line:
                idx_feature = idx_feature_pair.split(':')
                idx = idx_feature[0]
                feature = idx_feature[1]
                indices.append(int(idx))
                data.append(float(feature))
                pointer += 1
            idxptr.append(pointer)
        self.labels = np.asarray(labels, np.float64)
        self.feature_matrix = csr_matrix((data, indices, idxptr), dtype=np.float32)


if __name__ == '__main__':
    dl = SparseMatrixReader('../Data/ap89_training.txt')
    print dl.labels, type(dl.labels)
    print dl.feature_matrix.toarray()
