class Centroid(object):

    def __init__(self, x, w, id):
        self.mean = float(x)
        self.count = float(w)
        self.id = id

    def add(self, x, w):
        self.count += w
        self.mean += w * (x - self.mean) / self.count

    def equals(self, c):
        if c.id == self.id:
            return True
        else:
            return False

    def distance(self, x):
        return abs(self.mean - x)

    def __repr__(self):
        return "Centroid{centroid=%.1f, count=%d}" % (self.mean, self.count)
