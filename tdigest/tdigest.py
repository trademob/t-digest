import json

from random import shuffle

from .tdigestcore import TDigestCore


class TDigest(object):
    def __init__(self, delta=0.01, compression=20):
        self.delta = float(delta)
        self.compression = compression
        self.tdc = TDigestCore(self.delta)

    def add(self, x, w):
        self.tdc.add(x, w)
        if len(self) > self.compression / self.delta:
            self.compress()

    def compress(self):
        aux_tdc = TDigestCore(self.delta)
        centroid_list = self.tdc.centroid_list
        shuffle(centroid_list)
        for c in centroid_list:
            aux_tdc.add(c.mean, c.count)
        self.tdc = aux_tdc

    def quantile(self, x):
        return self.tdc.quantile(x)

    def serialize(self):
        centroids = [[c.mean, c.count] for c in self.tdc.centroid_list]
        return json.dumps(centroids)

    def __len__(self):
        return len(self.tdc)

    def __repr__(self):
        return str(self.tdc)
