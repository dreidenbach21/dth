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

# MY ITERATION LOOP BOUNDS ARE VERY BIG BUT THEY ALWASY PREMATERUALY STOP
# THIS MAY CAUSE ERRORS
# def test_and_return(v,last,G,mst,droploc,leafloc,cost, dfs_order, index, path):
#     # we have one drop off location left and we want to make sure that
#     # we take the min cost so thats whether we drop off the last one
#     min_cost = sys.maxsize
#     min_vertex = -1
#
#     i = index
#     print(last, " this is the last")
#     while i < len(dfs_order):
#
#         cur = dfs_order[i]
#         print(i, " this is our current node ", cur)
#         if(dfs_order[i] == last):
#             break
#         distance_home = nx.bellman_ford_path_length(G,0,cur)
#         print(distance_home, " distance home")
#         distance_drop = nx.bellman_ford_path_length(G,cur,last)
#         print(distance_drop, " distance to drop ", cur, last)
#         costa = 2/3*distance_home+distance_drop
#         if(costa < min_cost):
#             min_cost = costa
#             min_vertex = cur
#             print(min_vertex, " the updated min vertex")
#         i+=1
#
#
#     print(min_vertex, "WE HAVE OUR MIN")
#     i = index
#     print(dfs_order, " dfs order")
#     while i < len(dfs_order):
#         q = dfs_order[i]
#         if(q == min_vertex):
#             break
#         path.append(q)
#         print(q, " appending")
#         i+=1
#
#     cost+=min_cost
#     print(cost,"WE HAVE OUR cost")
#     # now need path from min to home
#     spaths = nx.shortest_path(G, source=min_vertex, target=0, weight='weight')
#     for ec in spaths:
#         path.append(ec)
#         print(ec, " appending")
#     print("WE HAVE OUR path")
#     print(path, " here is the path of the algorithm")
#     print(cost, " here is the total cost of the algorithm")

    # min_vertex is where we want to go then go home and drop from there


def find_drive_path(G,mst,dfs_order,droploc,leafloc,locs, cost):
    leaves = len(list(leafloc.keys()))
    for leaf in leafloc:
            drop = leafloc[leaf]
            spaths = nx.shortest_path(G, source=drop, target=leaf, weight='weight')
            extra = spaths[:]
            extra.pop(0)
            # print(spaths, " the shortest_path")
            count = {}
            # print(dfs_order, " the pre order")
            for ini in range(0,len(dfs_order)):
                lok = dfs_order[ini]
                if(lok in extra):
                    dfs_order[ini]=-1
                elif(lok not in count):
                    count[lok] = 1
                elif(lok in count and lok in spaths):
                    dfs_order[ini]=-1

            dfs_order = [word for word in dfs_order if word != -1]
            # print(dfs_order, " the post order")
            leaves-=1
    return dfs_order


def find_cost(mst,G,leafloc,droploc, cost,dfs_order):
    ta_cost = 1
    driver_cost = 2/3
    i = 0
    # print(dfs_order, " the dfs order")
    while i < len(dfs_order)-1:
        print(dfs_order[i],dfs_order[i+1])
        dist = nx.bellman_ford_path_length(G,dfs_order[i],dfs_order[i+1])
        cost += driver_cost*dist
        i+=1
    cost += driver_cost*nx.bellman_ford_path_length(G,dfs_order[-1],0)
    # Naive Driver Cost done
    # NO LAST DROP OPTIMIZATION
    for leaf in leafloc:
        dist = nx.bellman_ford_path_length(G,leaf,leafloc[leaf])
        # print(dist, leaf, leafloc[leaf])
        cost += ta_cost*dist
    # print(cost, "______COST_______")
def DTH(G,mst,dfs_order,droploc,leafloc,locs):
    cost = 0

    dfs_order = find_drive_path(G,mst,dfs_order,droploc,leafloc,locs,cost)
    # find_cost(mst,G,leafloc,droploc, cost,dfs_order)
    return dfs_order, droploc, leafloc

#     left_to_drop = {}
#     for leaf in leafloc:
#         left_to_drop[leaf] = 1
#
#     droplocations = len(list(left_to_drop.keys()))
#
#     path = []
#     seen = {}
#
# # THERE IS A HAS_PATH METHOD
#     i = 0
#     while i < len(dfs_order):
#         v = dfs_order[i]
#         u = dfs_order[i+1]
#
#         seen[v] = 1
#         print( v, u, " v and u")
#         print(cost, " cost top")
#
#
#         if(v in droploc):
#             # we have a location we want to drop
#             # update are next iteration
#             print("_________WE HAVE A DROP LOC_________")
#             if( droplocations == 1):
#                 print("_________FINAL DROP LOC_________")
#                 # we have one drop location left take us home and exit
#                 last = list(left_to_drop.keys())[0]
#                 test_and_return(v,last,G,mst,droploc,leafloc, cost, dfs_order, i, path)
#                 return cost
#             else:
#
#                 path.append(v)
#                 print(v, " appending")
#
#                 goodbye = droploc[v]
#                 for c in goodbye:
#                     if( droplocations == 1):
#                         # we have one drop location left take us home and exit
#                         print("_________FINAL DROP LOC_________")
#                         last = list(left_to_drop.keys())[0]
#                         test_and_return(v,last,G,mst,droploc,leafloc, cost, dfs_order, i, path)
#                         print("_________FINISHED_________")
#                         return cost
#
#                     else:
#                         distance = nx.bellman_ford_path_length(G,v,c)
#                         print(distance, " distance between")
#                         cost+= distance*ta_cost
#                         print(cost, "  cost b")
#                         droplocations-=1
#                         del left_to_drop[c]
#                         deleted_value = -1
#                         for k in range(0,len(dfs_order)):
#                             if(dfs_order[k] == c):
#                                 deleted_value = k
#                         j = i
#                         while(deleted_value >0):
#                             if(dfs_order[deleted_value] == v):
#                                 j = deleted_value
#                             deleted_value-=1
#                         # add all of the ones in the path to seen
#                         while j < len(dfs_order):
#                             print(dfs_order[j], "     SKIP     ")
#                             seen[dfs_order[j]] = 1
#                             if(dfs_order[j] == c):
#                                 break
#                             j+=1
#                         # BRING I TO BE THE NEWEST UNSEEN VERTEX IN THE DFS ORDER
#                         j = i
#                         while j < len(dfs_order):
#                             q = dfs_order[j]
#                             if(q not in seen):
#                                 break
#                             j+=1
#                         i = j#this is where we walk until we hit a new vertex
#                         # if(i>=len(dfs_order))
#                         u = dfs_order[i]
#                         print(u, " next")
#                         weight = G.get_edge_data(v, u)[0]['weight']
#                         cost+=weight*driver_cost
#
#         else:
#             path.append(v)
#             print(v, " appending")
#             # CAN WE ASSUME U WILL ALWAYS HAVE AN EDGE
#             # I THINK SO SINCE ITS BASED OFF A DFS
#             weight = G.get_edge_data(v, u)[0]['weight']
#             cost+=weight*driver_cost
#             print(cost, " cost bottom")
            # i+=1
