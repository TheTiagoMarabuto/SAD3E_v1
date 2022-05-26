import dearpygui.dearpygui as dpg
import dijkstra as dij
import tools as t

NODE_SIZE = 20
seen_nodes = []


def show_import_window(graph_file_path, plant_path, exit_array):
    ######################### VARIABLES #########################
    active_fires = []
    exit_list=[]
    graph = dij.build_graph(t.read_json(graph_file_path))  # build graph from .json filename
    dij.set_nearest_exit(graph, exit_array)  # run dijkstra and calculate all distances and paths
    #############################################################

    ######################### FUNCTIONS #########################
    # config function
    def _config(sender, app_data):
        if sender == "add_exit_array":
            a=5
        if sender == "node_listbox":
            exit_list.append(app_data)
            dpg.configure_item("exits_listbox", items=exit_list)
            list_aux=[node for node in graph]
            for i in exit_list:
                if i in list_aux:
                    list_aux.remove(i)
            dpg.configure_item("node_listbox", items=list_aux)

        if sender == "add_exits_button":
            exit_array=dpg.get_item_configuration("exits_listbox").get("items")
            dij.set_nearest_exit(graph, exit_array)
            dpg.configure_item("choose_exit_window", show=False)
            dpg.configure_item("run_simulation", enabled=True)

        if sender == "run_simulation":
            dpg.configure_item("fire_menu", enabled=True)
            dpg.configure_item("information_table", show=True)
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

    def _add_fire(sender):
        # get values from widgets
        node1 = dpg.get_value("node1_combo")
        node2 = dpg.get_value("node2_combo")
        intensity = dpg.get_value("input_intensity")

        # check if list is not empty
        if active_fires:
            for act_fire in active_fires:
                node1_aux, node2_aux, intensity_aux = act_fire.split(",")
                # check if fire already exists
                if (node1, node2) == (node1_aux, node2_aux) or (node1, node2) == (node2_aux, node1_aux):
                    # same nodes, same intensity
                    if intensity == int(intensity_aux):
                        print("INFO: Fire is already active")
                        # Close Popup
                        dpg.configure_item("add_fire_popup", show=False)

                        # Set widgets to initial states
                        dpg.configure_item("node1_combo", default_value="")
                        dpg.configure_item("node2_combo", show=False)
                        dpg.configure_item("input_intensity", default_value=0, show=False)

                    # same nodes, different intensity
                    else:
                        active_fires.remove(node1 + "," + node2 + "," + intensity_aux)  # remove fire from fire list
                        active_fires.append(node1 + "," + node2 + "," + str(intensity))  # add fire to fire list
                        dpg.configure_item("active_fires_list", items=active_fires)  # update active fires combo

                # Fire doesn't exist
                else:
                    # Add to active fires
                    if node1 + "," + node2 + "," + str(intensity) not in active_fires and node1 + "," + node2 + "," + str(intensity) not in active_fires:
                        active_fires.append(node1 + "," + node2 + "," + str(intensity))
                        dpg.configure_item("active_fires_list", items=active_fires)

        else:
            # Add to active fires
            if node1 + "," + node2 + "," + str(intensity) not in active_fires and node1 + "," + node2 + "," + str(intensity) not in active_fires:
                active_fires.append(node1 + "," + node2 + "," + str(intensity))
                dpg.configure_item("active_fires_list", items=active_fires)

        # Compute affected areas
        dij.affected_area(graph, graph[node1], graph[node2], intensity, exit_array)
        # Update information table
        for node in graph:
            tag = node + "_info"
            value = "Node: " + node + "->" + graph[node].next_node + "\ndistance to exit: " + str(graph[node].distance_to_exit) + "(" + graph[node].exit + ")"
            dpg.configure_item(tag, default_value=value)

        # show fire image to graph
        dpg.configure_item("fire_" + node1 + "_" + node2, show=True)

        # Close Popup
        dpg.configure_item("add_fire_popup", show=False)

        # Set widgets to initial states
        dpg.configure_item("node1_combo", default_value="")
        dpg.configure_item("node2_combo", show=False)
        dpg.configure_item("input_intensity", default_value=0, show=False)

    def _remove_fire(sender):
        # Get fire location
        fire = (dpg.get_value("active_fires_list").split(","))
        node1 = fire[0]
        node2 = fire[1]

        # Remove fire image and affected area
        dpg.configure_item("fire_" + node1 + "_" + node2, show=False)  # Remove fire image
        dij.remove_fire(graph, graph[node1], graph[node2])  # Remove affected area
        active_fires.remove(dpg.get_value("active_fires_list"))
        dpg.configure_item("active_fires_list", items=active_fires, default_value="")

        # Update information table
        for node in graph:
            tag = node + "_info"
            value = "Node: " + node + "->" + graph[node].next_node + "\ndistance to exit: " + str(graph[node].distance_to_exit) + "(" + graph[node].exit + ")"
            dpg.configure_item(tag, default_value=value)

    #############################################################

    dpg.create_context()
    #  load images (Plant, node, fire)

    width, height, channels, data = dpg.load_image(plant_path)
    width1, height1, channels1, data1 = dpg.load_image('/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/esfera.png')
    width2, height2, channels2, data2 = dpg.load_image('/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/fire.png')

    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="image_id")
        dpg.add_static_texture(width1, height1, data1, tag="sphere")
        dpg.add_static_texture(width2, height2, data2, tag="fire")

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

    # ###########################------------- MAIN WINDOW -------------############################
    with dpg.window(tag="main_window", label="Visualization", width=1200, height=-1, no_collapse=True, no_move=True):

        # add menu bar to window
        with dpg.menu_bar(tag="menu_bar", label="Menu Bar"):
            # File Menu
            with dpg.menu(tag="file_menu", label="File"):
                dpg.add_menu_item(tag="open", label="Open")

            # Run Menu
            with dpg.menu(tag="run_menu", label="Run"):
                dpg.add_menu_item(tag="add_exit_array", label="Exits", callback=_config)
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

            # Settings Menu
            with dpg.menu(tag="settings_menu", label="Settings"):
                # Toggle FullScreen Action
                dpg.add_menu_item(tag="toggle_fullscreen", label="Toggle Full screen", callback=lambda: dpg.toggle_viewport_fullscreen())

        # Next Node and Distance to Exit information TABLE
        with dpg.table(tag="information_table", label="Information Table", width=200, height=800, header_row=False, no_host_extendX=True, delay_search=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, context_menu_in_body=True, row_background=True, policy=dpg.mvTable_SizingFixedFit, scrollY=True, show=False):

            # Table with only one collumn
            dpg.add_table_column(width=200)

            # For each node in graph, add a table row
            for node in graph:
                with dpg.table_row():
                    dpg.add_text("Node: " + node + "->" + graph[node].next_node + "\ndistance to exit: " + str(graph[node].distance_to_exit) + "(" + graph[node].exit + ")", tag=node + "_info")

        # add plot with plant
        with dpg.plot(height=800, width=-1, pos=(200,)):
            # add X axis
            dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
            # add Y axis
            with dpg.plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_labels=True, no_tick_marks=True, tag="plot"):
                # Print Plant
                dpg.add_image_series("image_id", [0, 0], [1000, 800])
                # Go through nodes
                for node in graph:
                    # Go through edges
                    for dst, weight, hazard in graph[node].edges:
                        # Check if edge was already drew
                        if dst not in seen_nodes:
                            # Print edges
                            dpg.add_line_series((3*graph[node].location[0], 3*graph[dst].location[0]), (3*graph[node].location[1], 3*graph[dst].location[1]))
                            # get middle of edge
                            center = dij.get_center(graph[node].location, graph[dst].location)
                            # add fire image to graph
                            dpg.add_image_series("fire", (center[0] - 5, center[1] - 5), (center[0] + 5, center[1] + 5), tag="fire_" + node + "_" + dst, show=False)
                # Go through nodes
                for node in graph:
                    # Print nodes

                    dpg.add_image_series("sphere", (3*graph[node].location[0] - NODE_SIZE / 2, 3*graph[node].location[1] - NODE_SIZE / 2), (
                        3*graph[node].location[0] + NODE_SIZE / 2, 3*graph[node].location[1] + NODE_SIZE / 2), tag=node + "_image")  # Add label= to be able to hide nodes
            # Go through nodes
            for node in graph:
                # Print Node Name
                dpg.add_plot_annotation(label=node, default_value=graph[node].location[:2], offset=(0, 0), color=[0, 0, 255])

    # ###########################---------------------------------------############################
    # ###########################------------- CHOOSE EXIT WINDOW -------------############################
    with dpg.window(tag="choose_exit_window", label="Choose Exits", width=100, height=200, show=False):
        with dpg.group(horizontal=True):
            dpg.add_listbox([node for node in graph], tag="node_listbox", label="Nodes", callback=_config)
            dpg.add_listbox([], tag="exits_listbox", label="Nodes")
            dpg.add_button(tag="add_exits_button", label="Add Exits", callback=_config)
    # ###########################---------------------------------------############################






