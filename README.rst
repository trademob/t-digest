.. image:: https://travis-ci.org/trademob/t-digest.svg?branch=master
    :target: https://travis-ci.org/trademob/t-digest

Python implementation of t-digest algorithm
==========================================

t-digest is a online clustering algorithm for approximations of ranked-based statistics, such as the median or quantiles. The accuracy of calculated quantiles is proportional to `q * (1 - q)`, resulting in very accurate estimations of extreme quantiles. Furthermore this repo contains an evolution of that algorithm - called MergeDigest. 

The algorithm was first introduced by Ted Dunning. Further information can be found in the original `white paper <https://github.com/tdunning/t-digest/blob/master/docs/t-digest-paper/histo.pdf?raw=true>`_ or the `reference implementation of the algorithm in Java <https://github.com/tdunning/t-digest/>`_.


Installation
------------

.. code-block:: bash

    $ pip install git+https://github.com/trademob/t-digest.git


Usage
-----

.. code-block:: python

    from tdigest import TDigest
    from merge_digest import MergeDigest

    td = TDigest()
    td.add(0.54321, 1)  # adding new value to the storage
    ...  		# adding some more values here
    td.quantile(0.5)  # estimating median value

    md = MergeDigest()
    md.add(1,1)
    md.add(2,1)
    md.serialize()  # [[1, 1], [2, 1]]
