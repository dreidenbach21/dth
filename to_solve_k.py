import networkx as nx
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import sys
import numpy as np
from UnionFind import UnionFind
from UnionNode import UnionNode
from UnionPrim import UnionPrim
from KrusPrune import KrusPrune
def to_solve_k(G,locs):
    un = UnionFind()
    pos = 1

    source = UnionNode(0)
    dict = source.get_vertices()
    dict[0] = 0
    un.add(source)


    for l in locs:
        if l != 0:
            source = UnionNode(l)
            dict = source.get_vertices()
            dict[l] = pos
            un.add(source)
            pos+=1
    return KrusPrune(un, G,locs)
