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



def DropLoc(mst,G,source,locs,droploc,leafloc):
    # print("___FINDING DROP OFF LOCATIONS___")

    global leaves
    leaves = []
    traverse(mst,source,locs, None,droploc,leafloc, source)
    convert(leafloc,droploc)
    # print(droploc, " drop loc")
    # print(leafloc, " leaf loc")
    # print("___FOUND DROP___")
def convert(leafloc,droploc):
    for leaf in leafloc.keys():
        drop = leafloc[leaf]
        if drop not in droploc:
            droploc[drop] = [leaf]
        else:
            droploc[drop].append(leaf)
def traverse(mst,source,locs, parent, droploc,leafloc,home):
    # print(source, " the source")
    neighbors = list(mst.neighbors(source))
    global leaves
    # we use a global variable here since we want to be able to reset it glabally every time we use it

    if(parent != None):
        neighbors.remove(parent)
    # print(neighbors, " the neighbors")
    # print(leaves, " leaves")
    for n in neighbors:
        traverse(mst,n,locs,source,droploc,leafloc, home)
        # the below will handle the over 1 drop
        # print(source, " this is the source")
        # print(leaves, " leaves")
        # print(n, " this is the child")
        if(source == 0 and len(leaves)> 0 and n in locs):
            # weird case of never move
            # print("______CASE 0______")
            for leaf in leaves:
                leafloc[leaf] = source
            leaves = []
        if(len(leaves) > 0 and (len(neighbors) or source == home) > 1 and (len(list(set(leaves) & set(neighbors)))==0 )):
            # print("______CASE 1______")
            for leaf in leaves:
                leafloc[leaf] = source
            leaves = []
        # the below will handle the under 1 drop WE ARE SEEING IF ALL MY NEIGHTBORS ARE NOT HOMES
        if(len(leaves) > 0 and (len(neighbors) > 1 or source == home) and (not len(list(set(list(locs.keys())) & set(neighbors)))==len(neighbors)) ):
            # print("______CASE 2______")
            for leaf in leaves:
                leafloc[leaf] = source
            leaves = []

    if(len(neighbors) == 0 and source in locs):
        # print("___Found a special leaf___")
        leaves.append(source)
