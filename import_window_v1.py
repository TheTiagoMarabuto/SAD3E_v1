import dearpygui.dearpygui as dpg
import dijkstra as dij
import tools as t
import os
import modbusTCP as mb
from collections import defaultdict
import threading
import concurrent.futures
from time import sleep

NODE_SIZE = 20
DRAW_LAYER_SIZE = 1200

server_ip = '10.0.1.221'
port = 502

images_path = os.path.join(os.getcwd(), "Images")
node_image_path = os.path.join(images_path, "node.png")
fire_image_path = os.path.join(images_path, "fire.png")

font_dir = os.path.join(os.getcwd(), "Fonts")
default_font_path = os.path.join(font_dir, "ProductSans-Regular.ttf")
second_font_path = os.path.join(font_dir, "Arial Black.ttf")


def show_import_window(project_path):
    exit_array1 = []
    dpg.create_context()
    # ###########################-------------   FONT ASSIGNMENT  -------------########################
    with dpg.font_registry():
        default_font = dpg.add_font(default_font_path, 15)
        second_font = dpg.add_font(second_font_path, 20)
    dpg.bind_font(default_font)
    # ################################################################################################
    # ###########################-------------   GET PATHS  -------------########################
    graph_file_path = os.path.join(project_path, "graph.json")
    for root, dirs, files in os.walk(project_path):
        if "plant.png" in files:
            plant_path = os.path.join(project_path, "plant.png")
        if "plant.jpg" in files:
            plant_path = os.path.join(project_path, "plant.jpg")
        else:
            print("PLANT IMAGE NOT FOUND")
            return
    # ################################################################################################
    # ######################## VARIABLES #########################
    # start connection
    client = mb.MB_Client(server_ip, port)

    seen_nodes = []
    active_fires = []
    exit_list = []
    dev_available = []
    arrows = defaultdict()
    sensor_assignment = defaultdict()  # key (loop, device_number) | value x  (node1, node2)
    graph = dij.build_graph(t.read_json(graph_file_path))  # build graph from .json filename
    edges = dij.get_edges(graph)  # edges
    # #############################################################
    # ###########################-------------   TEXTURES  -------------##############################

    width, height, channels, data = dpg.load_image(plant_path)
    width1, height1, channels1, data1 = dpg.load_image(node_image_path)
    width2, height2, channels2, data2 = dpg.load_image(fire_image_path)

    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="plant_id")
        dpg.add_static_texture(width1, height1, data1, tag="node_pic")
        dpg.add_static_texture(width2, height2, data2, tag="fire_pic")

    # ##############################################################################################
    # ###########################-------------   FUNCTIONS  -------------############################
    def modbus_com(MBClient):
        dev_available = mb.available_devices(MBClient)

        while True:
            dev_states = mb.device_states(MBClient, dev_available)
            for loop, device_n, state in dev_states:
                # Alarm state = 3
                if state[0] == 3:
                    if (loop, device_n) in sensor_assignment:
                        (node1, node2) = sensor_assignment.get((loop, device_n))
                        if [node1, node2, 50] not in active_fires or [node2, node1, 50] not in active_fires:
                            _add_fire("modbus", [node1, node2, 50])
            dev_states.clear()
            sleep(10)

    def _assign_device():
        device = eval(dpg.get_value("dev_available_listbox"))
        edge = eval(dpg.get_value("edges_listbox"))
        sensor_assignment[device] = edge

    def get_draw_image_size(picture_width, picture_height):
        if picture_width >= DRAW_LAYER_SIZE:
            ratio = DRAW_LAYER_SIZE / picture_width
            if ratio * picture_height >= 800:
                ratio = 800 / picture_height
                return picture_width * ratio, 800
            else:
                return DRAW_LAYER_SIZE, picture_height * ratio
        if picture_height >= 800:
            ratio = 800 / picture_height
            if ratio * picture_width >= DRAW_LAYER_SIZE:
                ratio = DRAW_LAYER_SIZE / picture_width
                return DRAW_LAYER_SIZE, picture_height * ratio
            else:
                return picture_width * ratio, 800
        else:
            return DRAW_LAYER_SIZE, 800

    def _config(sender, app_data):
        if sender == "add_detector_devices":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(mb.available_devices, client)
                dpg.configure_item("dev_assignment_window", show=True)
                dev_available = future.result()

            dpg.configure_item("wait_text", show=False)
            dpg.configure_item("dev_assignment_window", no_close=False)
            dpg.configure_item("text_group", show=True)
            dpg.configure_item("listbox_group", show=True)
            dpg.configure_item("dev_available_listbox", items=[x[:2] for x in dev_available])
            dpg.configure_item("assign_device_button", show=True)

        if sender == "edges_listbox_arrow":
            items = dpg.get_item_configuration("arrow_listbox").get("items")
            if dpg.get_value(sender) not in items:
                items.append(dpg.get_value(sender))
                dpg.configure_item("arrow_listbox", items=items)

        if sender == "arrow_listbox":
            items = dpg.get_item_configuration("arrow_listbox").get("items")
            items.remove(dpg.get_value(sender))
            dpg.configure_item("arrow_listbox", items=items)

        if sender == "add_arrow_button":
            items = dpg.get_item_configuration("arrow_listbox").get("items")
            for node in items:
                draw_arrow(node)
            dpg.configure_item("choose_arrow_window", show=False)

        if sender == "exits_listbox":
            if app_data in exit_list:
                exit_list.remove(app_data)
                dpg.configure_item("exits_listbox", items=exit_list)
                list_aux = [node for node in graph]
                for i in exit_list:
                    if i in list_aux:
                        list_aux.remove(i)
                list_aux.sort()
                dpg.configure_item("node_listbox", items=list_aux)

        if sender == "node_listbox":
            exit_list.append(app_data)
            dpg.configure_item("exits_listbox", items=exit_list)
            list_aux = [node for node in graph]
            for i in exit_list:
                if i in list_aux:
                    list_aux.remove(i)
            list_aux.sort()
            dpg.configure_item("node_listbox", items=list_aux)

        if sender == "add_exits_button":
            exit_array1 = dpg.get_item_configuration("exits_listbox").get("items")
            dij.set_nearest_exit(graph, exit_array1)
            dpg.configure_item("choose_exit_window", show=False)
            dpg.configure_item("run_simulation", enabled=True)
            # Update table
            for node in graph:
                tag = node + "_info"
                value = "Node: " + node + "->" + graph[node].next_node + "\ndistance to exit: " + str(graph[node].distance_to_exit) + "(" + graph[node].exit + ")"
                dpg.configure_item(tag, default_value=value)
            for node in exit_array1:
                dpg.configure_item(node + "_image", fill=(255, 0, 0))

        if sender == "run_simulation":
            dpg.configure_item("fire_menu", enabled=True)
            dpg.configure_item("information_table", show=True)
            t = threading.Thread(target=modbus_com, args=(client,))
            t.start()
        if sender == "stop_simulation":
            dpg.configure_item("fire_menu", enabled=False)
        if sender == "node1_combo":
            dpg.configure_item("node2_combo", items=[edge[0] for edge in graph[app_data].edges], default_value="", show=True)
        if sender == "node2_combo":
            dpg.configure_item("input_intensity", show=True)
        if sender == "input_intensity":
            dpg.configure_item("add_fire_button", show=True)
        if sender == "active_fires_list":
            dpg.configure_item("remove_fire_button", show=True)
        if sender == "cancel_button":
            dpg.configure_item("add_fire_popup", show=False)
            # Set widgets to initial states
            dpg.configure_item("node1_combo", default_value="")
            dpg.configure_item("node2_combo", show=False)
            dpg.configure_item("input_intensity", default_value=0, show=False)

    def _add_fire(sender, user_data):
        if sender == "add_fire_button":
            # get values from widgets
            node1 = dpg.get_value("node1_combo")
            node2 = dpg.get_value("node2_combo")
            intensity = dpg.get_value("input_intensity")
        else:
            node1 = user_data[0]
            node2 = user_data[1]
            intensity = user_data[2]

        # check if list is not empty
        if active_fires:
            for act_fire in active_fires:
                # node1_aux, node2_aux, intensity_aux = act_fire.split(",")
                # check if fire already exists
                if [node1, node2] == act_fire[:2] or [node2, node1] == act_fire[:2]:  # (node1_aux, node2_aux) or (node1, node2) == (node2_aux, node1_aux):
                    # same nodes, same intensity
                    if intensity == act_fire[2]:
                        if sender == "add_fire_button":
                            print("INFO: Fire is already active")
                            # Close Popup
                            dpg.configure_item("add_fire_popup", show=False)

                            # Set widgets to initial states
                            dpg.configure_item("node1_combo", default_value="")
                            dpg.configure_item("node2_combo", show=False)
                            dpg.configure_item("input_intensity", default_value=0, show=False)

                    # same nodes, different intensity
                    else:
                        # active_fires.remove(node1 + "," + node2 + "," + intensity_aux)  # remove fire from fire list
                        active_fires.remove((node1, node2, act_fire[2]))
                        # active_fires.append(node1 + "," + node2 + "," + str(intensity))  # add fire to fire list
                        active_fires.append((node1, node2, intensity))
                        dpg.configure_item("active_fires_list", items=active_fires)  # update active fires combo

                # Fire doesn't exist
                else:
                    # Add to active fires
                    # if node1 + "," + node2 + "," + str(intensity) not in active_fires and node2 + "," + node1 + "," + str(intensity) not in active_fires:
                    #   active_fires.append(node1 + "," + node2 + "," + str(intensity))
                    #  dpg.configure_item("active_fires_list", items=active_fires)
                    if [node1, node2, intensity] not in active_fires and [node2, node1, intensity] not in active_fires:
                        active_fires.append([node1, node2, intensity])
                        dpg.configure_item("active_fires_list", items=active_fires)


        else:
            # Add to active fires
            # if node1 + "," + node2 + "," + str(intensity) not in active_fires and node1 + "," + node2 + "," + str(intensity) not in active_fires:
            #   active_fires.append(node1 + "," + node2 + "," + str(intensity))
            #  dpg.configure_item("active_fires_list", items=active_fires)
            if [node1, node2, intensity] not in active_fires and [node2, node1, intensity] not in active_fires:
                active_fires.append([node1, node2, intensity])
                dpg.configure_item("active_fires_list", items=active_fires)

        # Compute affected areas
        dij.affected_area(graph, graph[node1], graph[node2], intensity, dpg.get_item_configuration("exits_listbox").get("items"))

        # Update arrows

        update_arrows()

        # Update information table
        for node in graph:
            tag = node + "_info"
            value = "Node: " + node + "->" + graph[node].next_node + "\ndistance to exit: " + str(graph[node].distance_to_exit) + "(" + graph[node].exit + ")"
            dpg.configure_item(tag, default_value=value)

        # show fire image to graph
        if dpg.does_item_exist("fire_" + node1 + "_" + node2):
            dpg.configure_item("fire_" + node1 + "_" + node2, show=True)
        if dpg.does_item_exist("fire_" + node2 + "_" + node1):
            dpg.configure_item("fire_" + node2 + "_" + node1, show=True)

        if sender == "add_fire_button":
            # Close Popup
            dpg.configure_item("add_fire_popup", show=False)

            # Set widgets to initial states
            dpg.configure_item("node1_combo", default_value="")
            dpg.configure_item("node2_combo", show=False)
            dpg.configure_item("input_intensity", default_value=0, show=False)

    def _remove_fire(sender):
        # Get fire location
        fire = eval(dpg.get_value("active_fires_list"))  # (dpg.get_value("active_fires_list").split(","))
        node1 = fire[0]
        node2 = fire[1]

        # Remove fire image and affected area
        dpg.configure_item("fire_" + node1 + "_" + node2, show=False)  # Remove fire image
        dij.remove_fire(graph, graph[node1], graph[node2])  # Remove affected area
        active_fires.remove(eval(dpg.get_value("active_fires_list")))
        dpg.configure_item("active_fires_list", items=active_fires, default_value="")

        # Update information table
        for node in graph:
            tag = node + "_info"
            value = "Node: " + node + "->" + graph[node].next_node + "\ndistance to exit: " + str(graph[node].distance_to_exit) + "(" + graph[node].exit + ")"
            dpg.configure_item(tag, default_value=value)

    def draw_arrow(node):
        next_node = graph[node].next_node
        arrows[node] = next_node
        dpg.draw_arrow(graph[next_node].location[0:2], graph[node].location[0:2], parent="nodes_draw_layer", tag=f"{node}_{next_node}_arrow", show=True, color=(0, 255, 0), thickness=3)

    def update_arrows():
        aux = []
        for node in arrows:
            # check if arrow is shown
            if not dpg.does_item_exist(f"{node}_{graph[node].next_node}_arrow"):
                dpg.delete_item(f"{node}_{arrows[node]}_arrow")
                aux.append(node)
                next_node = graph[node].next_node
                dpg.draw_arrow(
                    graph[next_node].location[0:2], graph[node].location[0:2], parent="nodes_draw_layer", tag=f"{node}_{graph[node].next_node}_arrow", show=True, color=(0, 255, 0), thickness=3)
        for node in aux:
            arrows.pop(node)
            arrows[node] = graph[node].next_node

    def draw_node(node_pos, parent, node_name):
        dpg.draw_circle(node_pos, NODE_SIZE / 2, parent=parent, tag=node_name + "_image", color=(255, 255, 255), fill=(0, 144, 81), thickness=3)
        # dpg.draw_image("node_pic", (node_pos[0] - NODE_SIZE / 2, node_pos[1] - NODE_SIZE / 2), (node_pos[0] + NODE_SIZE / 2, node_pos[1] + NODE_SIZE / 2), parent=parent, tag=node_name + "_image")
        dpg.draw_text((node_pos[0] + NODE_SIZE / 2, node_pos[1] - NODE_SIZE / 2), node_name, parent=parent, tag=node_name + "_text", color=(0, 50, 255), size=22)  # color=(170, 70, 130), size=20)
        dpg.bind_item_font(node_name + "_text", second_font)

    def draw_edge(node1_name, node2_name, parent):
        dpg.draw_line(graph[node1_name].location[:2], graph[node2_name].location[0:2], tag=node1_name + "_" + node2_name + "_edge", parent=parent, color=(0, 0, 0), thickness=3)

    def draw_fire(node1_name, node2_name, parent):
        # get middle of edge
        center = dij.get_center(graph[node1_name].location, graph[node2_name].location)
        # add fire image to graph
        dpg.draw_image("fire_pic", (center[0] - NODE_SIZE / 2, center[1] - NODE_SIZE / 2), (
            center[0] + NODE_SIZE / 2, center[1] + NODE_SIZE / 2), parent=parent, tag="fire_" + node1_name + "_" + node2_name, show=False)

    def _draw_graph(sender):
        for node in graph:
            seen_nodes.append(node)
            draw_node(graph[node].location[0:2], "nodes_draw_layer", node)
            for dst, w, h in graph[node].edges:
                if dst not in seen_nodes:
                    draw_edge(node, dst, "edges_draw_layer")
                    draw_fire(node, dst, "nodes_draw_layer")

    # ##############################################################################################
    # ###########################------------- MAIN WINDOW -------------############################
    with dpg.window(tag="main_window", label="Visualization", width=1200, height=800, no_collapse=True, no_move=True):

        # add menu bar to window
        with dpg.menu_bar(tag="menu_bar", label="Menu Bar"):
            # File Menu
            with dpg.menu(tag="file_menu", label="File"):
                dpg.add_menu_item(tag="open", label="Open")

            # Run Menu
            with dpg.menu(tag="run_menu", label="Run"):
                dpg.add_menu_item(tag="draw_graph", label="Draw Graph", callback=_draw_graph)
                dpg.add_menu_item(tag="add_exit_array", label="Exits", callback=lambda: dpg.show_item("choose_exit_window"))
                dpg.add_menu_item(tag="add_arrows", label="Add Arrows", callback=lambda: dpg.show_item("choose_arrow_window"))
                dpg.add_menu_item(tag="add_detector_devices", label="Add Detectors", callback=_config)
                dpg.add_menu_item(tag="run_simulation", label="Run Simulation", callback=_config, enabled=False)
                dpg.add_menu_item(tag="stop_simulation", label="Stop Simulation", callback=_config, enabled=False)

            # Fire Menu
            with dpg.menu(tag="fire_menu", label="Fire", enabled=False):
                # Add Fire Action
                dpg.add_menu_item(tag="add_fire", label="Add Fire", callback=lambda: dpg.configure_item("add_fire_popup", show=True))

                # Remove Fire Action
                with dpg.menu(tag="remove_fire_menu", label="Remove Fire"):
                    dpg.add_combo(active_fires, tag="active_fires_list", label="Active Fires", callback=_config)
                    dpg.add_button(tag="remove_fire_button", label="Remove Fire", show=False, callback=_remove_fire)

            with dpg.menu(tag="info_menu", label="Information"):
                dpg.add_menu_item(tag="info_table_menu", label="See Information Table", callback=lambda: dpg.configure_item("info_table_window", show=True))

        # Draw layer bottom -> Plant ; middle -> edges ; top -> Nodes
        with dpg.draw_layer(tag="plant_layer", label="Plant Layer", parent="main_window"):
            dpg.draw_image("plant_id", pmin=(0, 0), pmax=get_draw_image_size(width, height))
        dpg.add_draw_layer(tag="edges_draw_layer", parent="main_window")
        dpg.add_draw_layer(tag="nodes_draw_layer", parent="main_window")

    # ###########################------------- CHOOSE EXIT WINDOW -------------############################
    with dpg.window(tag="choose_exit_window", label="Choose Exits", width=200, height=200, show=False, pos=(350, 200), modal=True):
        with dpg.group(horizontal=True):
            dpg.add_text("Nodes")
            dpg.add_spacer(width=10)
            dpg.add_text("Exits")
        with dpg.group(horizontal=True):
            aux = [node for node in graph]
            aux.sort()
            dpg.add_listbox(aux, tag="node_listbox", callback=_config, width=50, num_items=6)
            dpg.add_listbox([], tag="exits_listbox", width=50, num_items=6, callback=_config)
            dpg.add_button(tag="add_exits_button", label="Add Exits", callback=_config, width=60, pos=(120, 95))
    # ###########################---------------------------------------############################
    # ###########################------------- INFO TABLE WINDOW -------------############################
    with dpg.window(tag="info_table_window", label="Information Table", width=250, show=False, modal=True):
        # Next Node and Distance to Exit information TABLE
        with dpg.table(tag="information_table", label="Information Table", width=250, height=800, header_row=False, no_host_extendX=True, delay_search=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, context_menu_in_body=True, row_background=True, policy=dpg.mvTable_SizingFixedFit, scrollY=True, show=False):
            # Table with only one collumn
            dpg.add_table_column(width=250)

            # For each node in graph, add a table row
            for node in graph:
                with dpg.table_row():
                    dpg.add_text("", tag=node + "_info")
    # ###########################---------------------------------------############################
    # ###########################-------- ADD FIRE POPUP WINDOW --------############################
    with dpg.window(tag="add_fire_popup", label="Add Fire", pos=(500, 200), width=250, show=False, modal=True, no_title_bar=True, autosize=True, ):
        # Node 1 combo list
        dpg.add_combo([node for node in graph], tag="node1_combo", label="Node 1", default_value="", width=50, show=True, callback=_config)

        # Node 2 combo list
        dpg.add_combo(tag="node2_combo", label="Node 2", default_value="", width=50, show=False, callback=_config)

        # Hazard intensity setting
        dpg.add_input_int(tag="input_intensity", label="Hazard Intensity", width=100, show=False, callback=_config, min_value=50, min_clamped=True)  # input intensity between 50 and 100
        # Space between inputs and buttons
        dpg.add_separator()
        dpg.add_spacer()

        # Group with Cancel and Add Fire buttons
        with dpg.group(horizontal=True):
            dpg.add_button(tag="add_fire_button", label="Add Fire", show=False, callback=_add_fire)

            dpg.add_button(tag="cancel_button", label="Cancel", callback=_config)

    # ###########################---------------------------------------############################
    # ###########################-------- Device assignment window --------############################
    with dpg.window(tag="dev_assignment_window", label="Assign Devices", pos=(500, 200), width=300, height=300, show=False, no_collapse=True, no_close=True):
        dpg.add_text("waiting for modbus info....", tag="wait_text", pos=(60, 20), color=(255, 0, 0))
        with dpg.group(horizontal=True, show=False, tag="text_group"):
            dpg.add_text("(loop, device_number)")
            dpg.add_spacer(width=20)
            dpg.add_text("Edges")
        with dpg.group(horizontal=True, show=False, tag="listbox_group"):
            dpg.add_listbox(dev_available, tag="dev_available_listbox", width=120, num_items=10)
            dpg.add_listbox(edges, tag="edges_listbox", width=100, num_items=10)
        dpg.add_button(label="Assign Device", tag="assign_device_button", callback=_assign_device, show=False)

        # ###########################---------------------------------------############################
        # ###########################------------- CHOOSE ARROW PLACEMENT WINDOW -------------############################
        with dpg.window(tag="choose_arrow_window", label="Choose Arrow Placement", width=200, height=200, show=False, pos=(350, 200), modal=True):
            with dpg.group(horizontal=True):
                dpg.add_text("All Edges")
            with dpg.group(horizontal=True):
                dpg.add_listbox([node for node in graph], tag="edges_listbox_arrow", callback=_config, width=50, num_items=6)
                dpg.add_listbox([], tag="arrow_listbox", width=50, num_items=6, callback=_config)
                dpg.add_button(tag="add_arrow_button", label="Add Arrow", callback=_config, width=60, pos=(
                120, 95))  # ###########################---------------------------------------############################
