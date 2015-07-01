from setuptools import setup, find_packages
import codecs

import tdigest


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()

setup(
    name='tdigest',
    version=tdigest.__version__,
    description=tdigest.__doc__.strip(),
    long_description=long_description(),
    #download_url='https://github.com/trademob/python-tdigest',
    author=tdigest.__author__,
    #author_email='',
    license=tdigest.__licence__,
    packages=find_packages(),
    install_requires=[],
    tests_require=[
        'sure',
        'numpy',
        'nose',
        ],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ],
    )
