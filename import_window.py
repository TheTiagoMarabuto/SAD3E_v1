import dearpygui.dearpygui as dpg
import dijkstra as dij
import tools as t

NODE_SIZE = 20
seen_nodes = []


def show_import_window(graph_file_path, plant_path, exit_array):
    graph = dij.build_graph(t.read_json(graph_file_path))  # build graph from .json filename
    dij.set_nearest_exit(graph, exit_array)  # run dijkstra and calculate all distances and paths

    ######################### FUNCTIONS #########################
    # config function for choosing fire between nodes and intensity
    def _config(sender, app_data):
        if sender == "node1_combo":
            dpg.configure_item("node2_combo", items=[edge[0] for edge in graph[app_data].edges], default_value="", show=True)
        if sender == "node2_combo":
            dpg.configure_item("input_intensity", show=True)
        if sender == "input_intensity":
            dpg.configure_item("add_fire_button", show=True)

    def _add_fire(sender):
        # get values from widgets
        node1 = dpg.get_value("node1_combo")
        node2 = dpg.get_value("node2_combo")
        intensity = dpg.get_value("input_intensity")

        # Compute affected areas
        dij.affected_area(graph, graph[node1], graph[node2], intensity, exit_array)
        # Update information table
        for node in graph:
            tag = node + "_info"
            value = "Node: " + node + "->" + graph[node].next_node + "\ndistance to exit: " + str(graph[node].distance_to_exit) + "(" + graph[node].exit + ")"
            dpg.configure_item(tag, default_value=value)

        # show fire image to graph
        #dpg.add_image_series("fire", (center[0] - 5, center[1] - 5), (center[0] + 5, center[1] + 5), tag="fire_" + node1 + "_" + node2, parent="plot")
        dpg.configure_item("fire_" + node1 + "_" + node2, show=True)

        # Close Popup
        dpg.configure_item("add_fire_popup", show=False)

        # Set widgets to initial states
        dpg.configure_item("node1_combo", default_value="")
        dpg.configure_item("node2_combo", show=False)
        dpg.configure_item("input_intensity", default_value="", show=False)

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
        dpg.add_input_int(tag="input_intensity", label="Hazard Intensity", width=100, show=False, callback=_config)
        # Space between inputs and buttons
        dpg.add_separator()
        dpg.add_spacer()

        # Group with Cancel and Add Fire buttons
        with dpg.group(horizontal=True):
            dpg.add_button(tag="add_fire_button", label="Add Fire", show=False, callback=_add_fire)

            dpg.add_button(tag="cancel_button", label="Cancel", callback=lambda: dpg.configure_item("add_fire_popup", show=False))

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
                dpg.add_menu_item(tag="run_simulation", label="Run Simulation")
                dpg.add_menu_item(tag="stop_simulation", label="Stop Simulation")

            # Fire Menu
            with dpg.menu(tag="fire_menu", label="Fire"):
                # Add Fire Action
                dpg.add_menu_item(tag="add_fire", label="Add Fire", callback=lambda: dpg.configure_item("add_fire_popup", show=True))

                # Remove Fire Action
                dpg.add_menu_item(tag="remove_fire", label="Remove Fire")

            # Settings Menu
            with dpg.menu(tag="settings_menu", label="Settings"):
                # Toggle FullScreen Action
                dpg.add_menu_item(tag="toggle_fullscreen", label="Toggle Full screen", callback=lambda: dpg.toggle_viewport_fullscreen())

        # Next Node and Distance to Exit information TABLE
        with dpg.table(tag="information_table", label="Information Table", width=200, height=800, header_row=False, no_host_extendX=True, delay_search=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, context_menu_in_body=True, row_background=True, policy=dpg.mvTable_SizingFixedFit, scrollY=True):

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
                            dpg.add_line_series((graph[node].location[0], graph[dst].location[0]), (graph[node].location[1], graph[dst].location[1]))
                            # get middle of edge
                            center = dij.get_center(graph[node].location, graph[dst].location)
                            # add fire image to graph
                            dpg.add_image_series("fire", (center[0] - 5, center[1] - 5), (center[0] + 5, center[1] + 5), tag="fire_" + node + "_" + dst, show=False)
                # Go through nodes
                for node in graph:
                    # Print nodes
                    dpg.add_image_series("sphere", (graph[node].location[0] - NODE_SIZE / 2, graph[node].location[1] - NODE_SIZE / 2), (
                        graph[node].location[0] + NODE_SIZE / 2, graph[node].location[1] + NODE_SIZE / 2), tag=node + "_image")  # Add label= to be able to hide nodes
            # Go through nodes
            for node in graph:
                # Print Node Name
                dpg.add_plot_annotation(label=node, default_value=graph[node].location[:2], offset=(0, 0), color=[0, 0, 255])

    # ###########################---------------------------------------############################
