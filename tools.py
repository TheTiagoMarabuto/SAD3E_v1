# @author - Tiago Marabuto

import json
import dijkstra
from collections import defaultdict
import os
import pathlib
import shutil


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
    file = open(filepath_object, mode)
    json.dump(graph_to_dict(graph), file)
    file.close()


# save picture to json
def picture_to_json(filepath_object, picture_tag, picture_data):
    file = open(os.path.dirname(filepath_object) + "/pictures.json", "a")

    picture_dict = {picture_tag: {"width": picture_data[0], "height": picture_data[1], "channels": picture_data[2], "data": picture_data[3]}}
    json.dump(picture_dict, file)
    file.close()


# reads from filename and returns a dictionary
def read_json(filename):
    file = open(filename, "r")
    aux = json.load(file)
    file.close()
    return aux


def save_project_folder(name_path, plant_path, graph):

    dir = pathlib.Path(name_path)
    dir.mkdir(parents=True, exist_ok=True)
    write_json(os.path.join(dir, "graph.json"), "w", graph)

    plant_ext = os.path.splitext(plant_path)[1]
    plant = shutil.copy(plant_path, dir)
    os.rename(plant, os.path.join(os.path.dirname(plant), "plant" + plant_ext))



def graph_to_dict(graph):
    graph_dict = {node: {"dst": [], "weight": [], "hazard": [], "location": graph[node].location} for node in graph}

    for node in graph:
        for dst, weight, hazard in graph[node].edges:
            graph_dict[node]["dst"].append(dst)
            graph_dict[node]["weight"].append(weight)
            graph_dict[node]["hazard"].append(hazard)

    return graph_dict
