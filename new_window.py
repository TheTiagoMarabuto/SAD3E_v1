from collections import defaultdict

import dearpygui.dearpygui as dpg
import tools as t
import dijkstra as dij


def show_new_window(plant_path):
    dpg.create_context()
    # ###########################-------------   VARIABLES  -------------#############################
    graph = defaultdict(dij.Node)
    floor = 0 # Building floor is default to 0
    # ###########################---------------------------------------##############################
    # ###########################-------------   TEXTURES  -------------##############################
    width, height, channels, data = dpg.load_image(plant_path)
    width1, height1, channels1, data1 = dpg.load_image('C:\\Users\\tiago\\OneDrive\\Documentos\\GitHub\\SAD3E_v1\\images\\esfera.png')

    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="plant_id")
        dpg.add_static_texture(width1, height1, data1, tag="sphere")

    # ###########################---------------------------------------#############################
    # ###########################-------------   FUNCTIONS  -------------############################

    def _config(sender):
        if sender == "add_node_click":
            dpg.configure_item(handler, show=False)
            dpg.configure_item("add_node_window", show=True, pos=dpg.get_mouse_pos())
        if sender == "add_node_window":
            dpg.configure_item("node_name", default_value="")
            dpg.configure_item("node_exists_text", show=False)
            dpg.configure_item(handler, show=True)

    def _add_node(sender):
        a = 5

    def _remove_node(sender):
        a = 6

    def _draw_node_callback(sender):
        if not dpg.does_item_exist(dpg.get_value("node_name") + "_image"):
            draw_node(dpg.get_item_pos("add_node_window"), "draw_graph_layer", dpg.get_value("node_name"))
            # Hide window, set input to "" and enable mouse click
            dpg.configure_item("add_node_window", show=False)
            dpg.configure_item("node_name", default_value="")
            dpg.configure_item("node_exists_text", show=False)
            dpg.configure_item(handler, show=True)
        else:
            dpg.configure_item("node_exists_text", show=True)

    def draw_node(node_pos, parent, node_name):
        dpg.draw_image("sphere", (node_pos[0] - 20, node_pos[1] - 40), (node_pos[0], node_pos[1] - 20), parent=parent, tag=node_name + "_image")
        dpg.draw_text((node_pos[0], node_pos[1] - 40), node_name, parent=parent, tag=node_name + "_text", color=(255, 0, 0), size=20)
        write_to_graph(node_name, node_pos)

    def write_to_graph(node_name, pos):
        graph[node_name].name = node_name
        graph[node_name].location = (pos[0], pos[1], floor)

    def print_graph(graph):
        for node in graph:
            print(node)
    # ###########################---------------------------------------############################
    # ###########################-------------   HANDLERS  -------------############################
    with dpg.handler_registry(show=False) as handler:
        dpg.add_mouse_click_handler(button=0, callback=_config, parent="draw_graph_layer", tag="add_node_click")

    # ###########################---------------------------------------############################

    # ###########################------------- MAIN WINDOW -------------############################
    with dpg.window(tag="main_window", label="New Graph", width=1200, height=800, no_collapse=True, no_move=True, on_close=print_graph(graph)):
        # add menu bar to window
        with dpg.menu_bar(tag="menu_bar", label="Menu Bar"):
            # Add node button
            dpg.add_menu_item(tag="add_node", label="Add nodes", callback=lambda: dpg.configure_item(handler, show=True))
            dpg.add_menu_item(tag="stop_add_node", label="Stop Add nodes", callback=lambda: dpg.configure_item(handler, show=False))
            # Remove node button
            dpg.add_menu_item(tag="remove_node", label="Remove Node", callback=_remove_node)

        with dpg.draw_layer(tag="draw_graph_layer", label="Draw Graph Layer", parent="main_window"):
            dpg.draw_image("plant_id", pmin=(0, 0), pmax=(1200, 800))

    # ###########################---------------------------------------############################
    # ###########################----------- ADD NODE WINDOW -----------############################
    with dpg.window(tag="add_node_window", label="Node Name", width=100, height=110, show=False, no_move=True, modal=True, on_close=_config):
        dpg.add_input_text(tag="node_name")
        dpg.add_text("Node already exists!", tag="node_exists_text", show=False, wrap=100)
        dpg.add_button(tag="close_add_node_window", label="Create Node", callback=_draw_node_callback)
    # ###########################---------------------------------------############################
