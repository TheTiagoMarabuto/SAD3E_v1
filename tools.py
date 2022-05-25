# @author - Tiago Marabuto

import json
import dijkstra
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import os
import pylab


# creates JSON file with name = filename
def create_json_file(filename):
    try:
        file = open(filename, 'r')
        print("File already exists")
        file.close()
    except IOError:
        file = open(filename, 'w')
        file.close()


# writes dictionary to file with name filename
def write_json(filepath_object, mode, graph):
    file = open(os.path.basename(filepath_object), mode)
    json.dump(graph_to_dict(graph), file)
    file.close()


# save picture to json
def picture_to_json(filepath_object, picture_tag, picture_data):

    file = open(os.path.dirname(filepath_object)+"/pictures.json", "a")

    picture_dict = {picture_tag: {"width": picture_data[0], "height": picture_data[1], "channels": picture_data[2], "data": picture_data[3]}}
    json.dump(picture_dict, file)
    file.close()


# reads from filename and returns a dictionary
def read_json(filename):
    file = open(filename, "r")
    aux = json.load(file)
    file.close()
    return aux


def draw_graph(graph, fire_location=None):
    G = nx.Graph()
    # G.add_node("Fire", pos=fire_location[0:2])
    for node in graph:
        # name = node + "->" + graph[node].next_node
        G.add_node(node, pos=graph[node].location[0:2])
    seen_edges = defaultdict(int)
    for node in graph:
        for dst, weight, hazard in graph[node].edges:
            seen_edges[(node, dst)] += 1
            seen_edges[(dst, node)] += 1
            if seen_edges[(node, dst)] > 1:  # checking for duplicated edge entries
                continue
            G.add_edge(node, dst, weight=weight * hazard)

    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    pos = nx.get_node_attributes(G, 'pos')
    f, ax = plt.subplots(1, 1)
    if fire_location:
        circle1 = plt.Circle(fire_location, dijkstra.BIG_R, color='yellow')
        circle2 = plt.Circle(fire_location, dijkstra.SMALL_R, color='orange')
        ax.add_patch(circle1)
        ax.add_patch(circle2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, verticalalignment='bottom', bbox=dict(boxstyle='round', ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0), alpha=0))
    nx.draw(G, pos, node_size=180, with_labels=True, edge_cmap=plt.cm.Reds, font_size=8)
    # pylab.show()
    plt.tight_layout()
    plt.axis("off")

    plt.show()


def graph_to_dict(graph):
    graph_dict = {node: {"dst": [], "weight": [], "hazard": [], "location": graph[node].location} for node in graph}

    for node in graph:
        for dst, weight, hazard in graph[node].edges:
            graph_dict[node]["dst"].append(dst)
            graph_dict[node]["weight"].append(weight)
            graph_dict[node]["hazard"].append(hazard)

    return graph_dict
