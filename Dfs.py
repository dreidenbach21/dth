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


def Dfs(mst,G,locs,dfs_order,source):
    # print("___TRAVERSING___")
    visited = set()
    stack = deque()
    remove = []
    stack.append(source)

    traverse(mst,source,locs, None, dfs_order, visited)
    # print(dfs_order, " dfs order")
    # print("___TRAVERSED___")

def traverse(mst,source,locs, parent, dfs_order, visited):
    # print(source, " source vertex")
    # print(parent, " parent vertex")
    edges = list(mst.edges(source))
    if(parent != None):
        edges = [e for e in edges if not (e[0] == parent or e[1] == parent)]

    edges = sorted(edges, key=lambda edge: mst.get_edge_data(edge[0], edge[1])[0]['weight'])
    neigh = []
    for e in edges:
        if(e[0] == source):
            neigh.append(e[1])
        else:
            neigh.append(e[0])
    # WE NOW HAVE ALL OUR NEIGHBORS sorted
    # print(neigh, " sorted neighbors")
    dfs_order.append(source)
    visited.add(source)
    for child in neigh:
        if(child not in visited):
            traverse(mst,child,locs,source,dfs_order, visited)
        dfs_order.append(source)
