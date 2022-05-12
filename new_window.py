import dearpygui.dearpygui as dpg
import tools as t


def show_new_window(plant_path):
    # ###########################-------------   FUNCTIONS  -------------############################

    def _config(sender):
        if sender == "close_add_node_window":
            dpg.configure_item("add_node_window", show=False)
            dpg.configure_item("node_name", default_value="")
            dpg.configure_item(handler, show=True)
    def _add_node(sender):
        a = 5

    def _remove_node(sender):
        a = 6

    def _draw_node(sender):
        mouse_pos = dpg.get_mouse_pos()
        dpg.configure_item(handler, show=False)
        dpg.configure_item("add_node_window", show=True, pos=mouse_pos)

        node_name = dpg.get_value("node_name")
        dpg.draw_image("sphere", (mouse_pos[0]-20, mouse_pos[1]-40), (mouse_pos[0], mouse_pos[1]-20), parent="draw_graph_layer", tag=node_name + "_image")

    # ###########################---------------------------------------############################
    # ###########################-------------   HANDLERS  -------------############################
    with dpg.handler_registry() as handler:
        dpg.add_mouse_click_handler(button=0, callback=_draw_node, parent="draw_graph_layer", tag="add_node_click")


    # ###########################---------------------------------------############################
    dpg.create_context()
    width, height, channels, data = dpg.load_image(plant_path)
    width1, height1, channels1, data1 = dpg.load_image('/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/esfera.png')

    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="plant_id")
        dpg.add_static_texture(width1, height1, data1, tag="sphere")



    # ###########################------------- MAIN WINDOW -------------############################
    with dpg.window(tag="main_window", label="New Graph", width=1200, height=800, no_collapse=True, no_move=True):
        # add menu bar to window
        with dpg.menu_bar(tag="menu_bar", label="Menu Bar"):
            # Add node button
            dpg.add_menu_item(tag="add_node", label="Add node", callback=_add_node)
            # Remove node button
            dpg.add_menu_item(tag="remove_node", label="Remove Node", callback=_remove_node)

        with dpg.draw_layer(tag="draw_graph_layer", label="Draw Graph Layer"):
            dpg.draw_image("plant_id", pmin=(0, 0), pmax=(1200, 800))

    #dpg.bind_item_handler_registry("draw_graph_layer", "graph_click")
    # ###########################---------------------------------------############################
    # ###########################----------- ADD NODE WINDOW -----------############################
    with dpg.window(tag="add_node_window", label="Node Name", width=100, height=100, show=False):
        dpg.add_input_text(tag="node_name")
        dpg.add_button(tag="close_add_node_window", label="Create Node", callback=_config)
    # ###########################---------------------------------------############################