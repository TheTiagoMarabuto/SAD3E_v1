from collections import defaultdict

import dearpygui.dearpygui as dpg
import tools as t
import dijkstra as dij

node_image_path = "/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/node.png"


def show_new_window(plant_path):
    dpg.create_context()
    # ###########################-------------   FONT ASSIGNMENT  -------------########################
    with dpg.font_registry():
        default_font = dpg.add_font("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/Fonts/ProductSans-Regular.ttf", 15)
        second_font = dpg.add_font("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/Fonts/ProductSans-Bold.ttf", 20)
    dpg.bind_font(default_font)
    # ################################################################################################
    # ###########################-------------   VARIABLES  -------------#############################
    graph = defaultdict(dij.Node)
    floor = 0  # Building floor is default to 0
    # ##############################################################################################
    # ###########################-------------   TEXTURES  -------------##############################
    width, height, channels, data = dpg.load_image(plant_path)
    width1, height1, channels1, data1 = dpg.load_image(node_image_path)

    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="plant_id")
        dpg.add_static_texture(width1, height1, data1, tag="sphere")

    # ##############################################################################################
    # ###########################-------------   FUNCTIONS  -------------############################
    def get_draw_image_size(picture_width, picture_height):
        if picture_width >= 1200:
            ratio = 1200 / picture_width
            if ratio * picture_height >= 800:
                ratio = 800 / picture_height
                return picture_width * ratio, 800
            else:
                return 1200, picture_height * ratio
        if picture_height >= 800:
            ratio = 800 / picture_height
            if ratio * picture_width >= 1200:
                ratio = 1200 / picture_width
                return 1200, picture_height * ratio
            else:
                return picture_width * ratio, 800
        else:
            return 1200, 800

    def _config(sender, app_data, user_data):
        if sender == "add_node_click":
            dpg.configure_item(handler, show=False)
            dpg.configure_item(press_enter, show=True)
            dpg.configure_item("add_node_window", show=True, pos=dpg.get_mouse_pos())
        if sender == "add_node_window":
            dpg.configure_item("node_name", default_value="")
            dpg.configure_item("node_exists_text", show=False)
            dpg.configure_item(handler, show=True)
        if sender == "add_node":
            dpg.configure_item(handler, show=True)
            dpg.configure_item("add_node", check=True)
        if sender == "stop_add_node":
            dpg.configure_item(handler, show=False)
            dpg.configure_item("add_node", check=False)
        if sender == "edges_menu":
            dpg.configure_item("edges_listbox1", items=[node for node in graph])
            dpg.configure_item("add_edge_window", show=True, )
        if sender == "print_graph_button":
            if graph:
                print("Printing  Graph:")
                for node in graph:
                    print(node + str(graph[node].location))
                print("____ END ____")
            else:
                print("Graph still empty!")
        if sender == "save_graph_window":

            #t.picture_to_json(app_data.get("file_path_name"), "node_picture", (width1, height1, channels1, data1))
            #t.picture_to_json(app_data.get("file_path_name"), "plant", (width, height, channels, data))
            t.write_json(app_data.get("file_path_name") + user_data, "w", graph)


    def _remove_node(sender, app_data, user_data):
        # delete node image
        dpg.delete_item(user_data + "_image")
        # delete node text
        dpg.delete_item(user_data + "_text")

        #### DELETE EDGES !!!!!!!!!!!!

        # delete from graph
        graph.pop(user_data)
        dpg.configure_item("remove_node_window", show=False)

    def _draw_node_callback(sender):
        if not dpg.does_item_exist(dpg.get_value("node_name") + "_image"):
            draw_node(dpg.get_item_pos("add_node_window"), "nodes_draw_layer", dpg.get_value("node_name"))
            # Hide window, set input to "" and enable mouse click
            dpg.configure_item("add_node_window", show=False)
            dpg.configure_item("node_name", default_value="")
            dpg.configure_item("node_exists_text", show=False)
            dpg.configure_item(handler, show=True)
            dpg.configure_item(press_enter, show=False)
        else:
            dpg.configure_item("node_exists_text", show=True)

    def _draw_edge_callback(sender):
        node1 = dpg.get_value("edges_listbox1")
        node2 = dpg.get_value("edges_listbox2")
        distance = dij.distance_between_nodes(graph[node1], graph[node2])

        if (edge for edge in graph[node1].edges if edge[0] == node2):
            # add edge to graph
            graph[node1].edges.append((node2, distance, 1))
            graph[node2].edges.append((node1, distance, 1))
            update_listbox3_items()
            dpg.draw_line(graph[node1].location[:2], graph[node2].location[0:2], tag=node1 + "_" + node2 + "_edge", parent="edges_draw_layer", color=(0, 0, 0), thickness=5)

        else:
            dpg.configure_item("edge_exists_text", show=True)

        # UPDATE LISTBOX2 ITEMS AFTER ADD EDGE  # _update_listbox2_items()

    def _update_listbox2_items():
        list = [node for node in graph]
        list.remove(dpg.get_value("edges_listbox1"))
        if graph[dpg.get_value("edges_listbox1")].edges:
            for dst, weight, hazard in graph[dpg.get_value("edges_listbox1")].edges:
                list.remove(dst)
        dpg.configure_item("edges_listbox2", items=list)

    def update_listbox3_items():
        list = []
        for node in graph:
            for dst, weight, hazard in graph[node].edges:
                list.append(node + "->" + dst)
        dpg.configure_item("edges_listbox3", items=list)

    def draw_node(node_pos, parent, node_name):
        dpg.draw_image("sphere", (node_pos[0] - 20, node_pos[1] - 40), (node_pos[0], node_pos[1] - 20), parent=parent, tag=node_name + "_image")
        dpg.draw_text((node_pos[0], node_pos[1] - 40), node_name, parent=parent, tag=node_name + "_text", color=(170, 70, 130), size=20)
        dpg.bind_item_font(node_name + "_text", second_font)
        write_to_graph(node_name, node_pos)

    def write_to_graph(node_name, pos):
        graph[node_name].name = node_name
        graph[node_name].location = (pos[0] - 10, pos[1] - 27, floor)

    # ##############################################################################################
    # ###########################-------------   HANDLERS  -------------############################
    with dpg.handler_registry(show=False) as handler:
        dpg.add_mouse_click_handler(button=1, callback=_config, parent="draw_graph_layer", tag="add_node_click")
    with dpg.handler_registry(show=True) as press_enter:
        dpg.add_key_press_handler(key=76, callback=_draw_node_callback, parent="add_node_window", tag="draw_node_enter")

    # ##############################################################################################

    # ###########################------------- MAIN WINDOW -------------############################
    with dpg.window(tag="main_window", label="New Graph", width=1200, height=800, no_collapse=True, no_move=True):
        # add menu bar to window
        with dpg.menu_bar(tag="menu_bar", label="Menu Bar"):
            with dpg.menu(tag="edit_nodes", label="Nodes"):
                # Add node button
                dpg.add_menu_item(tag="add_node", label="Add nodes", callback=_config)
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text("After clicking, Right click to add nodes!")
                # Stop Add nodes
                dpg.add_menu_item(tag="stop_add_node", label="Stop Add nodes", callback=_config)
                # Remove node button
                dpg.add_menu_item(tag="remove_node", label="Remove Node", callback=lambda: dpg.configure_item("remove_node_window", show=True))

            dpg.add_menu_item(tag="edges_menu", label="Edges", callback=_config)
            with dpg.menu(tag="graph_menu", label="Graph"):
                dpg.add_menu_item(tag="print_graph_button", label="Print Graph", callback=_config)
                dpg.add_menu_item(tag="export_graph", label="Export", callback=lambda: dpg.configure_item("save_graph_window", show=True))

        # Draw layer bottom -> Plant ; middle -> edges ; top -> Nodes
        with dpg.draw_layer(tag="draw_graph_layer", label="Draw Graph Layer", parent="main_window"):
            dpg.draw_image("plant_id", pmin=(0, 0), pmax=get_draw_image_size(width, height))
        dpg.add_draw_layer(tag="edges_draw_layer", parent="main_window")
        dpg.add_draw_layer(tag="nodes_draw_layer", parent="main_window")
    # ##############################################################################################

    # ###########################----------- ADD NODE WINDOW -----------############################
    with dpg.window(tag="add_node_window", label="Node Name", width=100, height=-1, show=False, no_move=True, modal=True, on_close=_config):
        dpg.add_input_text(tag="node_name")
        dpg.add_text("Node already exists!", tag="node_exists_text", show=False, wrap=100)
        dpg.add_button(tag="close_add_node_window", label="Create Node", callback=_draw_node_callback)
    # ##############################################################################################

    # ###########################----------- REMOVE NODE WINDOW -----------#########################
    with dpg.window(tag="remove_node_window", label="Remove Nodes", width=150, height=150, show=False, pos=(500, 200)):
        dpg.add_listbox([node for node in graph], tag="nodes_listbox", num_items=5)
        dpg.add_button(tag="remove_node_button", label="Remove Node", callback=_remove_node, user_data=dpg.get_value("nodes_listbox"))
    # ##############################################################################################

    # ###########################----------- ADD EDGE WINDOW -----------############################
    with dpg.window(tag="add_edge_window", label="Add Edges", width=300, height=200, show=False, pos=(350, 200), modal=True):
        with dpg.group(horizontal=True):
            dpg.add_text("Node1")
            dpg.add_spacer(width=10)
            dpg.add_text("Node2")
            dpg.add_spacer(width=50)
            dpg.add_text("Edge")
        with dpg.group(horizontal=True):
            dpg.add_listbox([node for node in graph], tag="edges_listbox1", width=50, num_items=8, callback=_update_listbox2_items)
            dpg.add_listbox([""], tag="edges_listbox2", width=50, num_items=8, callback=lambda: dpg.configure_item("add_edge_button", show=True))
            with dpg.group():
                dpg.add_button(tag="add_edge_button", label="Add\nedge", callback=_draw_edge_callback)
                dpg.add_text(tag="edge_exists_text", label="Edge\nalready\nexists!", show=False)
            dpg.add_listbox([""], tag="edges_listbox3", width=60, num_items=8)
            dpg.add_button(tag="remove_edge_button", label="Remove\n edge")

    # ##############################################################################################
    # ###########################----------- SAVE DIALOG -----------############################
    with dpg.file_dialog(label="Save Graph", width=300, height=400, callback=_config, show=False, tag="save_graph_window", user_data=".json"):
        dpg.add_file_extension("JSON(.json){.json}", color=(0, 255, 0, 255))

    # #############################################################################################
