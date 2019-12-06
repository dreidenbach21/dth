import networkx as nx
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import random
import sys
import numpy as np
from UnionFind import UnionFind
from UnionNode import UnionNode
from UnionPrim import UnionPrim
from collections import deque

# L R Root post order
def Prune(mst,G,locs,source):
    # print("___PRUNING___")
    visited = {}
    stack = deque()
    remove = []
    stack.append(source)

    traverse(mst,source,locs, None)
    # print("___PRUNED___")

def traverse(mst,source,locs, parent):
    neighbors = list(mst.neighbors(source))
    # print(neighbors)
    if(parent != None):
        neighbors.remove(parent)
    for n in neighbors:
        traverse(mst,n,locs,source)

    neighbors = list(mst.neighbors(source))
    if(parent != None):
        neighbors.remove(parent)
    if(len(neighbors) == 0 and source not in locs):
        mst.remove_node(source)
        # print("___Removed A Node___")
