from collections import defaultdict

import dearpygui.dearpygui as dpg
import tools as t
import dijkstra as dij

graph = dij.build_graph(t.read_json("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/edges.json"))
exit_array = ["U", "S"]
dij.set_nearest_exit(graph, exit_array)

x_nodes = []
y_nodes = []

for node in graph:
    x_nodes.append(graph[node].location[0])
    y_nodes.append(graph[node].location[1])

WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
GOLD = (255, 215, 0)
seen_nodes = []
node_label = defaultdict()
edge_label = defaultdict()
dpg.create_context()
fire_nodes = [2]

##### variables

add_fire_popup_node1 = None
add_fire_popup_node2 = None
add_fire_popup_hazard_intensity = None


def _get_node(sender, app_data, user_data):
    if user_data == 1:
        fire_nodes[0] = app_data
        print(fire_nodes[0])
    if user_data == 2:
        fire_nodes[1] = app_data


def _config(sender, app_data):
    if app_data in graph:
        dpg.configure_item("node2", items=[edge[0] for edge in graph[app_data].edges], default_value="", show=True)

def _set_node2(sender, app_data):
    add_fire_popup_node2 = app_data
    dpg.configure_item("input_intensity", show = True)


def _add_fire(sender):
    app_data = [dpg.get_value("node1"), dpg.get_value("node2"), dpg.get_value("input_intensity")]
    dij.affected_area(graph, graph[app_data[0]], graph[app_data[1]], app_data[2], exit_array)
    center = dij.get_center(graph[app_data[0]].location, graph[app_data[1]].location)
    dpg.add_image_series("fire", (center[0]-5, center[1]-5), (center[0]+5, center[1]+5), tag="fire_" + app_data[0] + "_" + app_data[1], parent="plot")
    dpg.configure_item("add_fire_popup", show=False)


def _set_hazard_intensity(sender, app_data):
    add_fire_popup_hazard_intensity = app_data
    dpg.configure_item("add_fire_button", show=True)


############# ADD FIRE WINDOW ######################
with dpg.window(label="add_fire_popup", modal=True, show=False, id="add_fire_popup", no_title_bar=True, pos=(500, 200), width=250):
    all_nodes = []
    # possible_second_node = []

    for node in graph:
        all_nodes.append(node)

    dpg.add_combo([node for node in graph], callback=_config, default_value="", width=50, label="Node 1", tag="node1")
    dpg.add_combo(default_value="", callback=_set_node2, tag="node2", width=50, label="Node 2", show=False)
    dpg.add_input_int(label="Fire intensity", callback=_set_hazard_intensity, width=100, show=False, tag="input_intensity")
    dpg.add_button(label="Add Fire", tag="add_fire_button", show=False, pos=(100,), callback=_add_fire)
    dpg.add_button(label="Cancel", callback=lambda: dpg.configure_item("add_fire_popup", show=False))

#######################################################

width, height, channels, data = dpg.load_image('/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/feup_planta_900.png')
width1, height1, channels1, data1 = dpg.load_image('/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/esfera.png')
width2, height2, channels2, data2 = dpg.load_image('/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/fire.png')

with dpg.texture_registry():
    dpg.add_static_texture(width, height, data, tag="image_id")
    dpg.add_static_texture(width1, height1, data1, tag="sphere")
    dpg.add_static_texture(width2, height2, data2, tag="fire")

with dpg.window(label="Visualization", width=1200, height=-1, no_collapse=True, no_move=True, tag="main_window"):
    # add menu bar to window
    with dpg.menu_bar(label="menu_bar"):
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Open")
        with dpg.menu(label="Run"):
            dpg.add_menu_item(label="Run Simulation")
            dpg.add_menu_item(label="Stop Simulation")
        with dpg.menu(label="Fire"):
            dpg.add_menu_item(label="Add Fire", callback=lambda: dpg.configure_item("add_fire_popup", show=True))
            dpg.add_menu_item(label="Remove Fire")
        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Toggle Fullscreen", callback=lambda: dpg.toggle_viewport_fullscreen())
    with dpg.table(header_row=False, no_host_extendX=True, delay_search=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, context_menu_in_body=True, row_background=True, policy=dpg.mvTable_SizingFixedFit, width=200, height=800, scrollY=True):
        dpg.add_table_column(width=200)
        for node in graph:
            with dpg.table_row():
                dpg.add_text("Node: " + node + "->" + graph[node].next_node + "\ndistance to exit: " + str(graph[node].distance_to_exit) + "(" + graph[node].exit + ")")

    with dpg.plot(height=800, width=-1, pos=(200,)):
        dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        with dpg.plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_labels=True, no_tick_marks=True, tag="plot"):
            dpg.add_image_series("image_id", [0, 0], [1000, 800])
            for node in graph:
                for dst, weight, hazard in graph[node].edges:
                    # Check if edge was already drew
                    if dst not in seen_nodes:
                        dpg.add_line_series((graph[node].location[0], graph[dst].location[0]), (graph[node].location[1], graph[dst].location[1]))
            for node in graph:
                dpg.add_image_series("sphere", (graph[node].location[0] - 10, graph[node].location[1] - 10), (
                    graph[node].location[0] + 10, graph[node].location[1] + 10), tag=node + "_image")  # label=node+"_image") Uncomment to add ability to hide nodes

        for node in graph:
            dpg.add_plot_annotation(label=node, default_value=3 * graph[node].location[:2], offset=(0, 0), color=[255, 0, 255])

dpg.create_viewport(title='SAD3E', width=1200, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
