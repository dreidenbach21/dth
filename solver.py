import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import networkx as nx
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from UnionFind import UnionFind
from UnionNode import UnionNode
from UnionPrim import UnionPrim
from PrimPrune import PrimPrune
from to_solve import to_solve
from to_solve_k import to_solve_k

from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    orig_name_to_num = {}
    orig_num_to_name = {}
    for i in range(len(list_of_locations)):
        orig_name_to_num[list_of_locations[i]] = i
        orig_num_to_name[i] = list_of_locations[i]

    name_to_num = {}
    name_to_num[starting_car_location] = 0
    num_to_name = {}
    num_to_name[0] = starting_car_location
    counter = 1
    for location in list_of_locations:
        if(location != starting_car_location):
            name_to_num[location] = counter
            num_to_name[counter] = location
            counter += 1

    locs = {}
    locs[0] = 0
    counter2 = 1
    for home in list_of_homes:
        if home != starting_car_location:
            locs[name_to_num[home]] = counter2
            counter2 += 1

    edgeList = []
    # print(list_of_locations, " list of locations ")
    # print(adjacency_matrix)
    for i in range(len(list_of_locations)):
        for j in range(len(list_of_locations)):
            matWeight = adjacency_matrix[i][j]
            if matWeight == 'x':
                matWeight = 0
            else:
                matWeight = float(matWeight)
            if matWeight != 0:
                C = orig_num_to_name[i]
                start = name_to_num[C]
                D = orig_num_to_name[j]
                end = name_to_num[D]
                edgeList.append((start, end, matWeight))


    # print( orig_name_to_num, " orig_name_to_num")
    # print( orig_num_to_name, " orig_num_to_name")
    # print( name_to_num, " name_to_num")
    # print( num_to_name, " num_to_name")

    G = nx.MultiGraph()
    G.add_nodes_from(list(num_to_name.keys()))
    G.add_weighted_edges_from(edgeList)
    dfs_order, droploc, leafloc = to_solve_k(G, locs)
    # print("__________ DONE WITH ALG__________")
    if(dfs_order[-1] != dfs_order[0]):
        dfs_order.append(dfs_order[0])
    for leaf in leafloc:
        dr = leafloc[leaf]
        if dr not in dfs_order:
            min_dist = sys.maxsize
            vert = 0
            for drop in dfs_order:
                dis = nx.bellman_ford_path_length(G,drop,leaf)
                if( dis < min_dist):
                    vert = drop
                    min_dist = dis
            leafloc[leaf] = vert
            if vert not in droploc:
                droploc[vert]= [leaf]
            else:
                droploc[vert].append(leaf)

    drive_path = []
    for v in dfs_order:
        char = num_to_name[v] # taking our v and turning it into a char
        p = orig_name_to_num[char] # taking the char and returning the true adj matrix index
        drive_path.append(p)
    # print("__________test__________")
    # print(drive_path)
    homes = set(locs.keys())
    homes.remove(0)

    # while (len(list(homes & set(leafloc.keys())))== len(list(homes))):
    for loc in locs:
        if loc !=0 and loc not in leafloc:
            vert = 0
            min_dist = sys.maxsize
            for drop in dfs_order:
                dis = nx.bellman_ford_path_length(G,drop,leaf)
                if( dis < min_dist):
                    min_dist = dis
                    vert = drop
            leafloc[loc] = vert
            droploc[vert].append(loc)


    drop_locations = {}
    for drop in droploc:
        locations = []
        char = num_to_name[drop] # taking our v and turning it into a char
        p = orig_name_to_num[char] # taking the char and returning the true adj matrix index

        for col in droploc[drop]:
            charr = num_to_name[col] # taking our v and turning it into a char
            pp = orig_name_to_num[charr] # taking the char and returning the true adj matrix index
            locations.append(pp)
        drop_locations[p] = locations

    # print(drop_locations)
    # print("__________SOLVED__________")


    return drive_path, drop_locations






"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
