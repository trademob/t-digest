from __future__ import division

import json
import math
import sys


class MergeDigest(object):

    def __init__(self, compression=200):
        self.compression = compression
        # maximum number of new datapoints before merging
        self.buffer_size = self.estimate_buffer_size(compression)
        # temporary buffer for incoming data points
        self.temp_elements = []
        # working buffer during merging
        self.merge_elements = []
        # "final" centroid list
        self.elements = []

        self.total_weight = 0
        self.unmerged_weight = 0
        self.min = sys.maxint
        self.max = -sys.maxint

    def estimate_buffer_size(self, compression):
        if compression < 20:
            compression = 20
        elif compression > 1000:
            compression = 1000
        return int(7.5 + 0.37 * compression - 2e-4 * compression * compression)

    def add(self, x, w):
        # merge buffer if full
        if len(self.temp_elements) >= self.buffer_size:
            self.merge_new_values()

        # add new element to buffer
        self.temp_elements.append((x, w))
        self.unmerged_weight += w

    def merge_new_values(self):
        if not self.unmerged_weight:
            # no weight to merge
            return None

        # combine new "temp" elements with existing centroids and sort list
        self.temp_elements.extend(self.elements)
        self.temp_elements = sorted(
            self.temp_elements, key=lambda element: element[0])

        w_so_far = 0
        k1 = 0
        self.total_weight += self.unmerged_weight
        for el in self.temp_elements:
            w_so_far += el[1]
            k1 = self.merge_centroid(w_so_far, k1, el)

        # store merged centroids and reset buffer
        self.temp_elements = []
        self.unmerged_weight = 0
        self.elements = self.merge_elements
        self.merge_elements = []

        # get min/max of distribution
        if self.total_weight > 0:
            self.min = min(self.min, self.elements[0][0])
            self.max = max(self.max, self.elements[-1][0])

    def merge_centroid(self, w_so_far, k1, centroid):
        k2 = self.integrated_location(float(w_so_far) / self.total_weight)
        (mean, weight) = centroid
        if len(self.merge_elements) == 0:
            self.merge_elements.append((mean, weight))
            return k1
        (mean_before, weight_before) = self.merge_elements[-1]

        if (k2 - k1 <= 1):
            # merge into existing centroid
            weight_after = weight_before + weight
            mean_after = mean_before + (mean - mean_before) * float(weight) / weight_after
            self.merge_elements[-1] = (mean_after, weight_after)
        else:
            # create new centroid
            self.merge_elements.append((mean, weight))
            k1 = self.integrated_location(float(w_so_far - weight) / self.total_weight)

        return k1

    def quantile(self, q):
        if not 0 < q < 1:
            return None

        self.merge_new_values()

        n = len(self.elements)
        # handle case for zero or one centroids
        if n == 0:
            return None
        elif n == 1:
            return self.elements[0][0]

        index = q * self.total_weight

        right = self.min
        b = self.elements[0][0]
        b_count = self.elements[0][1]
        weight_so_far = 0

        for i in range(1, n):
            a = b
            a_count = b_count
            left = right
            b = self.elements[i][0]
            b_count = self.elements[i][1]
            right = float(b_count * a + a_count * b) / (a_count + b_count)

            if index < weight_so_far + a_count:
                p = float(index - weight_so_far) / a_count
                return float(left) * (1 - p) + right * p

            weight_so_far += a_count

        left = right
        a_count = b_count
        right = self.max

        if index < weight_so_far + a_count:
            p = float(index - weight_so_far) / a_count
            return float(left) * (1 - p) + right * p
        else:
            return self.max

    def cdf(self, x):
        self.merge_new_values()

        n = len(self.elements)

        if n == 0:
            return None
        elif n == 1:
            if x < self.min:
                return 0
            elif x > self.max:
                return 1
            elif self.max == self.min:
                return 0.5
            else:
                return (float(x - self.min) / (self.max - self.min))
        else:
            # handle case for 2+ centroids
            r = 0
            a = self.min
            b = self.min
            b_count = 0
            right = 0
            for i in range(n):
                left = b - (a + right)
                a = b
                a_count = b_count

                b = self.elements[i][0]
                b_count = self.elements[i][1]
                right = (b - a) * float(a_count) / (a_count + b_count)

                if x < a + right:
                    value = float(r + a_count * self.interpolate(x, a - left, a + right)) / self.total_weight
                    if value > 0:
                        return value
                    else:
                        return 0

                r += a_count
            left = b - (a + right)
            a = b
            a_count = b_count
            right = self.max - a

            if x < a + right:
                return float(r + a_count * self.interpolate(x, a - left, a + right)) / self.total_weight
            else:
                return 1

    def integrated_location(self, q):
        return float(self.compression) * (math.asin(2 * q - 1) + math.pi / 2) / math.pi

    def interpolate(self, val, left, right):
        return float(val - left) / (right - left)

    def serialize(self):
        self.merge_new_values()
        centroids = [(c[0], c[1]) for c in self.elements]
        return json.dumps(centroids)
