import dearpygui.dearpygui as dpg
from tools import *

graph = read_json("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/edges.json")
WHITE = (255, 255, 255)
seen_nodes = []
node_label = defaultdict()
edge_label = defaultdict()
dpg.create_context()
dpg.create_viewport(title="SAD3E - Run")

with dpg.window(no_collapse=True, width=1000, height=800) as window:
    # Add draw layer to window
    draw_layer = dpg.add_draw_layer()

    # Loop through all nodes and draw in draw_layer parent
    for node in graph:
        node_label[node] = dpg.draw_circle(center=(graph[node].get("location")[0], graph[node].get("location")[1]),
                                           radius=5, parent=draw_layer, fill=WHITE)

        seen_nodes.append(node)
        for edge in graph[node].get("dst"):
            # Check if edge was already drew
            if edge not in seen_nodes:
                edge_label[(node, edge)] = dpg.draw_line(
                    (graph[node].get("location")[0], graph[node].get("location")[1]),
                    (graph[edge].get("location")[0], graph[edge].get("location")[1]), parent=draw_layer)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
