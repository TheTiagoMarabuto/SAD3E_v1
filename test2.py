import dearpygui.dearpygui as dpg

from tools import *
from dijkstra import *

graph= build_graph(read_json("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/edges.json"))
exit_array = ["U", "S"]
set_nearest_exit(graph, exit_array)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
GOLD = (255, 215, 0)
seen_nodes = []
node_label = defaultdict()
edge_label = defaultdict()
dpg.create_context()

# callback runs when user attempts to connect attributes
def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)

# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    # app_data -> link_id
    dpg.delete_item(app_data)

with dpg.window(label="Tutorial", width=400, height=400):

    with dpg.node_editor(label="parent", callback=link_callback, delink_callback=delink_callback):
        for node in graph:
            seen_nodes.append(node)
            for dst, weight, hazard in graph[node].edges:
                # Check if edge was already drew
                if dst not in seen_nodes:
                    a=5
                    #edge_label[(node, dst)] = dpg.draw_line((30, 30), (50,50), label="HELLO", parent="parent")
                        #(graph[node].location[0], graph[node].location[1]),
                        #(graph[dst].location[0], graph[dst].location[1]), color=GOLD)


            # First draw edges and then the nodes
            with dpg.node(label=node, pos=(graph[node].location[0]*5,600-graph[node].location[1]*3),
                          draggable=False):

                dpg.add_node_attribute(label="in", shape=dpg.mvNode_PinShape_Triangle)

                with dpg.node_attribute(label="out", attribute_type=dpg.mvNode_Attr_Output,
                                        shape=dpg.mvNode_PinShape_Triangle):
                    dpg.add_text("Next:" + graph[node].next_node)

            #dpg.add_node_link(26,24)


dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()