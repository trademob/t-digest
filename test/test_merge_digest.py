import numpy as np
import sys
import unittest

from random import random
from sure import expect
from time import time

from tdigest.merge_digest import MergeDigest


class TestMergeDigest(unittest.TestCase):

    def stub_cdf(self, x, data):
        n1 = 0
        n2 = 0
        for el in data:
            if el < x:
                n1 += 1
            if el <= x:
                n2 += 1
        return (n1 + n2) / 2.0 / len(data)

    def stub_distribution_test(self, values):
        start = time()
        for value in values:
            self.md.add(value, 1)
        end = time()
        t_per_datapoint = float(end - start) / len(values)
        print 'Time per datapoint addition in microseconds: %f\n' % (t_per_datapoint * 10**6)
        values = sorted(values)
        print 'Quantile\tDistr q value\tMergeDigest q value\tdifference'
        soft_error = 0
        for quantile in self.quantiles:
            q_value_raw_distribution = np.percentile(values, quantile * 100)
            q_value_md = self.md.quantile(quantile)
            quantile_estimate = self.md.cdf(q_value_md)
            expect(quantile_estimate - quantile).to.be.below(0.005)
            quantile_estimate_with_q_value = self.stub_cdf(q_value_md, values)
            expect(quantile - quantile_estimate_with_q_value).to.be.below(0.012)
            if abs(quantile - quantile_estimate_with_q_value) > 0.005:
                soft_error += 1

            diff = abs(q_value_raw_distribution - q_value_md)
            print '%f\t%f\t%f\t%f' % (quantile, q_value_raw_distribution, q_value_md, diff)

        expect(soft_error).to.be.below(3)

    def setUp(self):
        self.compression = 500
        self.trials = 100
        self.datapoints = 100000
        self.quantiles = [0.0001, 0.001, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 0.999, 0.9999]
        self.md = MergeDigest(self.compression)

    def tearDown(self):
        self.md = None

    def test_serialization(self):
        for i in range(3):
            self.md.add(i, 1)
        expect(self.md.serialize()).to.be.equal('[[0, 1], [1, 1], [2, 1]]')

    def test_values_uniform(self):
        """
        Test with uniform distribution in (0, 1)
        """
        print TestMergeDigest.test_values_uniform.__doc__
        values = [random() for _ in range(self.datapoints)]
        self.stub_distribution_test(values)

    def test_values_standard_normal(self):
        """
        Test with Gaussian(0, 1)
        """
        print TestMergeDigest.test_values_standard_normal.__doc__
        values = [np.random.normal() for _ in range(self.datapoints)]
        self.stub_distribution_test(values)

    def test_values_gamma(self):
        """
        Test with Gamma(0.1)
        """
        print TestMergeDigest.test_values_gamma.__doc__
        values = [np.random.gamma(0.1, 10) for _ in range(self.datapoints)]
        self.stub_distribution_test(values)

    def test_values_narrow_normal(self):
        """
        Mixture of Uniform and Gaussian
        """
        print TestMergeDigest.test_values_narrow_normal.__doc__
        values = []
        for _ in range(self.datapoints):
            criteria = random()
            if criteria < 0.5:
                values.append(criteria)
            else:
                values.append(np.random.normal())
        self.stub_distribution_test(values)

    def test_values_sequence_asc(self):
        """
        Test with sequential datapoints (ascending)
        """
        print TestMergeDigest.test_values_sequence_asc.__doc__
        values = []
        c = 0
        step = 1.0 / (self.datapoints + 1)
        for _ in range(self.datapoints):
            c += step
            values.append(c)
        self.stub_distribution_test(values)

    def test_values_sequence_desc(self):
        """
        Test with sequential datapoints (descending)
        """
        print TestMergeDigest.test_values_sequence_desc.__doc__
        values = []
        c = 1.0
        step = 1.0 / (self.datapoints + 1)
        for _ in range(self.datapoints):
            c -= step
            values.append(c)
        self.stub_distribution_test(values)
