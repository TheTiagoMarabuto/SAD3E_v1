import dearpygui.dearpygui as dpg
from tools import *
from dijkstra import *

# graph = read_json("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/edges.json")
graph = build_graph(read_json("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/edges.json"))
exit_array = ["U", "S"]
set_nearest_exit(graph, exit_array)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
seen_nodes = []
node_label = defaultdict()
edge_label = defaultdict()
dpg.create_context()
dpg.create_viewport(title="SAD3E - Run")

width, height, channels, data = dpg.load_image(
    '/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/feup_planta_900.png')  # 0: width, 1: height, 2: channels,
# 3: data

with dpg.texture_registry():
    dpg.add_static_texture(width, height, data, tag="image_id")

with dpg.window(no_collapse=True, width=1000, height=800) as window:
    # add menu bar to window
    with dpg.menu_bar(label="menu_bar"):
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Open")
        with dpg.menu(label="Run"):
            dpg.add_menu_item(label="Run Simulation")
            dpg.add_menu_item(label="Stop Simulation")
        with dpg.menu(label="Fire"):
            dpg.add_menu_item(label="Add Fire")
            dpg.add_menu_item(label="Remove Fire")

    with dpg.drawlist(width=1000, height=800):
        dpg.draw_image("image_id", (0, 0), (width, height), uv_min=(0, 0), uv_max=(1, 1))
        # Add draw layer to window
        with dpg.draw_layer(tag="graph_layer"):
            # Loop through all nodes and draw in draw_layer parent
            for node in graph:
                seen_nodes.append(node)
                for dst, weight, hazard in graph[node].edges:
                    # Check if edge was already drew
                    if dst not in seen_nodes:
                        edge_label[(node, dst)] = dpg.draw_line((graph[node].location[0], graph[node].location[1]),
                            (graph[dst].location[0], graph[dst].location[1]), color=BLUE)
                # First draw edges and then the nodes
                node_label[node] = dpg.draw_circle(center=(graph[node].location[0], graph[node].location[1]), radius=8,
                    fill=ORANGE, tag=node)
                dpg.draw_text(pos=(graph[node].location[0] - 5, graph[node].location[1] - 5), text=node, color=BLACK)

                ## CHECK ERROR
                #with dpg.tooltip(parent=node):
                 #   dpg.draw_text(pos=(graph[node].location[0] - 5, graph[node].location[1] - 5),
                  #                text="Next Node: " + graph[node].next_node)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
