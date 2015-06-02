#!/usr/bin/env python3
import sys
import json
from lib.ascii_graph import Pyasciigraph


import numpy as np
from scipy.stats import kde
from scipy.signal import argrelextrema


from pprint import pprint

def compute_and_persist_maxima(f):
    words = json.load(open(f))
    # words_with_maxima = words
    for w in words:
        word = w['word']
        positions = w['positions']
        freq = w['freq']
        if len(positions) > 1:
            # print(maxima(positions))
            w['maxima'], w['graph'] = maxima(positions)
    # pprint(words)

    json.dump(words, open(f, 'w'), indent=2)

def maxima(positions):
    """ get variable amount of local maxima for the density distribution function  """

    X = np.array(positions)
    density = kde.gaussian_kde(X)
    xgrid = np.linspace(X.min(), X.max(), len(X))
    xgrid_fine = np.linspace(X.min(), X.max(), len(X)*10)
    local_maxima = X[argrelextrema(density(xgrid), np.greater)[0]]


    r =list(zip(map(lambda x: x/1000,xgrid_fine),[x*100 for x in density(xgrid_fine)]))
    return local_maxima.tolist(), r

    # graph = Pyasciigraph()
    # for line in  graph.graph('r', r):
    #     print(line)
    # pprint(local_maxima)

def main():
    args = sys.argv[1:]
    f = args[0] # output by wordtimings
    compute_and_persist_maxima(f)

main()
