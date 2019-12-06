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


def UnionPrim(un, G,locs):
    # 1)Create a set mstSet that keeps track of vertices already included in MST.
    # locs is a hashmap that maps the source/home to its unionfind element index
    edges = []
    vertices = set()
    for loc in locs.keys():
        vertices.add(loc)


    # 2) Assign a key value to all vertices in the input graph. Initialize all key values as INFINITE. Assign key value as 0 for the first vertex so that it is picked first.
    while(un.n_comps > 1):
        for loc in locs.keys():
            if(un.n_comps == 1):
                break
            numero = un.find(un.__getitem__(locs.get(loc)))
            node = un.__getitem__(numero)
            # print(node.label," this is the current location")
            vert_neigh = []
            edge_neigh = []
            ngv = node.get_vertices()

            optimze = []
            for vert in ngv:
                count = 0
                total = 0
                n = G.neighbors(vert)
                # print(list(n), " neighbors")
                for v in n:
                    # print(v, " the vertex line 41")
                    if( v not in ngv):
                        vert_neigh.append(v)
                        e=[vert,v]
                        # print(e, " edge for Prim")
                        edge_neigh.append(e)
                    else:
                        count+=1
                    total+=1
                if(count == total):
                    optimze.append(vert)
            for ver in optimze:
                ngv.pop(ver, None)
                # if all of my neighbots are already in the set remove me from the set


            # neighbors now has all valid neighbors that are not in the current set
            min = sys.maxsize
            min_vert = -1
            min_edge = -1
            # print(edge_neigh, " edge_neigh")
            # print(vert_neigh, " vert_neigh")

            # we want a way to equally shuffle two arrays
            # this randomization will more likely give better mst
            # rander = randint(0, 9)

            for i in range(len(vert_neigh)):
                edge = edge_neigh[i]
                vert = vert_neigh[i]
                # print(edge, " the edge in the size comp")
                # print(vert, " the vert in the size comp")
                # weightd = G.edges[edge[0], [edge[1]]
                ed = G.get_edge_data(edge[0], edge[1])
                # print(ed)
                weight = ed[0]['weight']
                # print(weight, " the weight of the edge")
                a = 0
                # print(vert, " the current vertex")
                if(vert in locs):
                    # print("____________IN____________")
                    a = .0000001
                if(weight-a < min):
                    print("UPDATE ", vert)
                    min = weight
                    min_vert = vert
                    min_edge = edge

            # now we have our min vertex and min weight we want to add
            vertices.add(min_vert)
            edges.append(min_edge)

            # now we want to union and merge
            for l in locs.keys():
                if(l==loc):
                    continue
                node2 = un.__getitem__(locs.get(l))
                # print(node2.get_vertices(), " POTENTIAL UNION")
                if(min_vert in node2.get_vertices()):
                    # print("UNION")
                    un.union(node,node2)
                    par = un.find(node)
                    parent = un.__getitem__(par)
                    if parent.label == node.label:
                        parent.vertices.update(node2.get_vertices())
                        parent.edges.update(node2.get_edges())
                    else:
                        parent.vertices.update(node.get_vertices())
                        parent.edges.update(node.get_edges())

            # print(min_vert, " the min vertex")
            numero = un.find(un.__getitem__(locs.get(loc)))
            node = un.__getitem__(numero)
            nvdic = node.get_vertices()
            nvdic[min_vert] = min_vert;
            nedic = node.get_edges()
            ned = (min_edge[0], min_edge[1])
            print(ned)
            nedic[ned] = ned;


    fin = []
    fin.append(vertices)
    fin.append(edges)
    # print(fin)
    return fin
