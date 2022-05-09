import dearpygui.dearpygui as dpg
import tools as t


def show_new_window(plant_path):
    # ###########################-------------   FUNCTIONS  -------------############################

    def _config(sender):
        a = 5

    def _add_node(sender):
        a=5

    def _remove_node(sender):
        a=6
    # ###########################---------------------------------------############################
    dpg.create_context()
    width, height, channels, data = dpg.load_image(plant_path)

    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="image_id")


    # ###########################------------- MAIN WINDOW -------------############################
    with dpg.window(tag="main_window", label="New Graph", width=1200, height=-1, no_collapse=True, no_move=True):
        # add menu bar to window
        with dpg.menu_bar(tag="menu_bar", label="Menu Bar"):
            # Add node button
            dpg.add_menu_item(tag="add_node", label="Add node", callback=_add_node)
            # Remove node button
            dpg.add_menu_item(tag="remove_node", label="Remove Node", callback=_remove_node)


        with dpg.plot(height=800, width=-1, pos=(200,)):

            # add X axis
            dpg.add_plot_axis(dpg.mvXAxis)
            # add Y axis
            with dpg.plot_axis(dpg.mvYAxis, tag="plot"):
                # Print Plant
                dpg.add_image_series("image_id", [0, 0], [1000, 800])
                dpg.add_line_series([0,50,100,150,300], [0,50,100,150,300] )
            dpg.add_plot_axis(dpg.mvYAxis)
            dpg.add_drag_point(color=(255, 0, 0), default_value=(50, 50), tag="point")
        #with dpg.plot(height=800, width=-1, pos=(200,)):
         #   dpg.add_plot_axis(dpg.mvXAxis,  no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
          #  dpg.add_plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_labels=True, no_tick_marks=True)

    # ###########################---------------------------------------############################
