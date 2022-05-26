# @author - Tiago Marabuto
import heapq
import math
from collections import defaultdict
from fibheap import *

BIGINT = 1806199818061998
SMALL_R = 100
BIG_R = 200


class Node:
    def __init__(self, name=None, location=None, next_node=None, distance_to_exit=BIGINT, exit=None):
        self.name = name
        self.next_node = next_node
        self.distance_to_exit = distance_to_exit
        self.exit = exit
        self.edges = []
        self.location = location  # node (x, y, z), with z being the floor in which the node is located

    def set_distance(self, distance_to_exit):
        self.distance_to_exit = distance_to_exit

    def set_next_node(self, next_node):
        self.next_node = next_node

    def get_distance(self):
        return self.distance_to_exit

    def get_next_node(self):
        return self.next_node

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location


# build graph given edges dictionary. Returns list of Node objects
def build_graph(edges):
    graph = defaultdict(Node)
    seen_edges = defaultdict(int)
    for src in edges:
        for dst, weight, hazard in zip(edges.get(src).get("dst"), edges.get(src).get("weight"),
                                       edges.get(src).get("hazard")):
            seen_edges[(src, dst)] += 1
            # seen_edges[(dst,src)] += 1
            if seen_edges[(src, dst)] > 1:  # checking for duplicated edge entries
                continue
            graph[src].edges.append((dst, weight, hazard))
            # print(src, dst, weight, hazard)
            # graph[dst].edges.append((src, weight, hazard))
        graph[src].location = edges.get(src).get("location")
        graph[src].name = src
    return graph


# calculates distance from src_node to all nodes. returns distance dictionary and prev array
def dijkstra_distance(graph, src_node):
    dist = dict()
    prev = dict()
    for node in graph:
        dist[node] = float('inf')
        prev[node] = None

    dist[src_node] = 0

    heap = [(dist[src_node], src_node)]
    seen = set()
    while heap:
        dist1, node = heapq.heappop(heap)
        if node not in seen:
            seen.add(node)
            for dst, weight, hazard in graph[node].edges:
                if dist[dst] > dist[node] + weight * hazard:
                    dist[dst] = dist[node] + weight * hazard
                    prev[dst] = node
                    heapq.heappush(heap, (dist[dst], dst))

    return dist, prev


# Set nearest exit and next node
def set_nearest_exit(graph, exit_array):
    for node in graph:
        graph[node].set_distance(BIGINT)
    for exit in exit_array:
        distance, prev = dijkstra_distance(graph, exit)
        for node in graph:
            path = find_path(prev, node)
            if graph[node].get_distance() > distance[node]:
                graph[node].set_distance(distance[node])
                graph[node].exit = exit
                if exit != node:
                    graph[node].set_next_node(path[1])
                else:
                    graph[node].set_next_node(path[0])


# distance between nodes in the same floor
def distance_between_nodes(nodeA, nodeB):
    # check if nodes are in the same floor
    if nodeA.location[2] == nodeB.location[2]:
        return math.sqrt((nodeA.location[0] - nodeB.location[0]) ** 2 + (nodeA.location[1] - nodeB.location[1]) ** 2)
    else:
        print("Can't calculate distance between: ", nodeA, "and", nodeB)


def change_hazard_intensity(nodeA, nodeB, hazard_intensity, graph, exit_array):
    for dst, weight, hazard in nodeA.edges:
        if dst == nodeB.name:
            nodeA.edges.remove((dst, weight, hazard))
            nodeB.edges.remove((nodeA.name, weight, hazard))

            nodeA.edges.append((dst, weight, hazard_intensity))
            nodeB.edges.append((nodeA.name, weight, hazard_intensity))

            nodeA.set_distance(BIGINT)
            nodeB.set_distance(BIGINT)

            set_nearest_exit(graph, exit_array)


# generate path list based on parent points pr and the node name
def find_path(pr, node):
    p = []
    aux = node
    while aux is not None:
        p.append(aux)
        aux = pr[aux]
    return p  # [::-1]  # Inverted array


def in_circle(center, R, node_location):
    dx = abs(center[0] - node_location[0])
    if dx > R:
        return False
    dy = abs(center[1] - node_location[1])
    if dy > R:
        return False
    if dx + dy <= R:
        return True
    return dx * dx + dy * dy <= R * R


def same_floor(center, node_location):
    return center[2] == node_location[2]


def get_center(nodeA_location, nodeB_location):
    center = ((nodeA_location[0] + nodeB_location[0]) / 2, (nodeA_location[1] + nodeB_location[1]) / 2, (nodeA_location[2] + nodeB_location[2]) / 2)
    return center


def affected_area(graph, nodeA, nodeB, hazard_intensity, exit_array):
    hazard_location = get_center(nodeA.location, nodeB.location)

    seen_nodes = []
    seen_edges = []

    for node in graph:

        if in_circle(hazard_location, SMALL_R, graph[node].location) and node not in seen_nodes:
            for dst, weight, hazard in graph[node].edges:
                if ((node == nodeA.name and dst == nodeB.name) or (dst == nodeA.name and node == nodeB.name)) and (dst,
                                                                                                                   node) not in seen_edges:  # ((hazard != 0.5 * hazard_intensity) and (hazard != 0.25 * hazard_intensity)):
                    index1 = graph[node].edges.index((dst, weight, hazard))

                    graph[node].edges.remove((dst, weight, hazard))
                    graph[node].edges.insert(index1, (dst, weight, hazard_intensity))
                    seen_edges.append((node, dst))

                    graph[dst].edges.remove((node, weight, hazard))
                    graph[dst].edges.append((node, weight, hazard_intensity))  # ????
                    seen_edges.append((dst, node))

                else:
                    index1 = graph[node].edges.index((dst, weight, hazard))
                    graph[node].edges.remove((dst, weight, hazard))
                    graph[dst].edges.remove((node, weight, hazard))
                    graph[node].edges.insert(index1, (dst, weight, 0.5 * hazard_intensity))
                    graph[dst].edges.append((node, weight, 0.5 * hazard_intensity))

            seen_nodes.append(node)

        if in_circle(hazard_location, BIG_R, graph[node].location) and node not in seen_nodes:
            for dst, weight, hazard in graph[node].edges:

                if (dst,
                    node) not in seen_edges:  # (hazard != 0.5 * hazard_intensity) and (hazard != 0.25 * hazard_intensity):
                    index1 = graph[node].edges.index((dst, weight, hazard))

                    graph[node].edges.remove((dst, weight, hazard))
                    graph[node].edges.insert(index1, (dst, weight, 0.25 * hazard_intensity))
                    seen_edges.append((node, dst))

                    graph[dst].edges.remove((node, weight, hazard))
                    graph[dst].edges.append((node, weight, 0.25 * hazard_intensity))
                    seen_edges.append((dst, node))

            seen_nodes.append(node)

    set_nearest_exit(graph, exit_array)

def remove_fire(graph, nodeA, nodeB):
    hazard_location = get_center(nodeA.location, nodeB.location)

    seen_nodes = []
    seen_edges = []

    for node in graph:
        if in_circle(hazard_location, BIG_R, graph[node].location):
            for dst, weight, hazard in graph[node].edges:
                index1 = graph[node].edges.index((dst, weight, hazard))
                graph[node].edges.remove((dst, weight, hazard))
                graph[node].edges.insert(index1, (dst, weight, 1))
