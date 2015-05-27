Python implementation of t-digest algorithm
==========================================

t-digest is a online clustering algorithm for approximations of ranked-based statistics, such as the median or quantiles. The accuracy of calculated quantiles is proportional to `q * (1 - q)`, resulting in very accurate estimations of extreme quantiles. 

The algorithm was first introduced by Ted Dunning. Further information can be found in the original `white paper <https://github.com/tdunning/t-digest/blob/master/docs/t-digest-paper/histo.pdf?raw=true>`_ or the `reference implementation of the algorithm in Java <https://github.com/tdunning/t-digest/>`_.


Usage
-----

.. code-block:: python

    from tdigest import TDigest

    td = TDigest()
    td.add(0.54321, 1)  # adding new value to the storage
    ...  		# adding some more values here
    td.quantile(0.5)  # estimating median value
