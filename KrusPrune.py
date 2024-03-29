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
from Dfs import Dfs
from Prune import Prune
from DropLoc import DropLoc
from DTH import DTH
from kruskals import Kruskals

def KrusPrune(un, G,locs):
    mst = Kruskals(un, G, locs)
    # print(soln, " the output of UnionPrim")


    Prune(mst,G,locs,0)
    # now all useless paths in our MST have been cut
    droploc = {}
    leafloc = {}
    DropLoc(mst,G,0,locs,droploc,leafloc)
    dfs_order = []
    Dfs(mst,G,locs,dfs_order,0)
    # print("_______STARTING TO DTH_______")
    # print(droploc, "_____droploc0____")
    dfs_order, droploc, leafloc = DTH(G,mst,dfs_order,droploc,leafloc,locs)
    # print(droploc, "_____droploc1____")
    for l in locs:
        if l not in leafloc and l != 0:
            leafloc[l] = l
            if l in droploc:
                droploc[l].append(l)
            else:
                droploc[l] = [l]
    # print(leafloc, "_____leafloc____")

    # for leaf in leafloc.keys():
    #     drop = leafloc[leaf]
    #     if drop not in droploc:
    #         droploc[drop] = [leaf]
    #     else:
    #         droploc[drop].append(leaf)
    # print(droploc, "_____droploc2____")
    # nx.shortest_path(G, source=min_vertex, target=0, weight='weight')






    # _____________DRAWING_____________

    # pos=nx.spring_layout(mst)
    # labels={}
    # for e in mst.edges():
    #     ed = G.get_edge_data(e[0], e[1])
    #     weight = ed[0]['weight']
    #     labels[(e[0], e[1])] = weight
    #
    # nx.draw_networkx_edge_labels(mst, pos, edge_labels = labels)
    # val_map = {}
    # for key in locs:
    #     val_map[key] = 'red'
    # values = [val_map.get(node, 'blue') for node in mst.nodes()]
    # nx.draw(mst, pos, node_color = values, with_labels = True)
    # plt.show()


    return dfs_order, droploc, leafloc

     # create the MST as a MultiGraph
     # DFS and prune paths that do not hit any homes
     # record locations of union leaves drop off nodes
        # if dfs(v) returns a list mark curr v as drop loc for home that is a leaf
