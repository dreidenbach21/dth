import networkx as nx
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
import random
import sys
import numpy as np
from UnionFind import UnionFind
from UnionNode import UnionNode
# from random import randint


def Kruskals(un, G,locs):
    # 1)Create a set mstSet that keeps track of vertices already included in MST.
    # locs is a hashmap that maps the source/home to its unionfind element index
    T = nx.minimum_spanning_tree(G, weight='weight', algorithm='kruskal')
    return T
