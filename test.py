from random import random
import unittest
from tdigest import TDigest
from tdigest.tdigestcore import TDigestCore


class TestTDigest(unittest.TestCase):

    def test_add(self):
        """Added value is saved"""
        td = TDigest(delta=0.1)
        self.assertEqual(td.tdc.centroidList, [])

        td.add(0.5, 1)
        self.assertEqual(len(td), 1)
        self.assertEqual(str(td.tdc.centroidList), '[Centroid{centroid=0.5, count=1}]')

    def test_compress(self):
        """Call compress() after reaching len(tdigest) > compression / delta"""
        pass

    def test_quantile(self):
        """Quantile calculation"""
        pass


class TestTDigestCore(unittest.TestCase):

    def test__closest_centroids(self):
        """Closest centroids are calculated properly"""
        pass

    def test__centroid_quantile(self):
        """Quantile for centroid is calculated properly"""

if __name__ == "__main__":
    unittest.main()
