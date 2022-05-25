import dearpygui.dearpygui as dpg
import dijkstra as dij
import tools as t


def show_import_window(graph_file_path, plant_path, exit_array):
    dpg.create_context()
    # ###########################-------------   FONT ASSIGNMENT  -------------########################
    with dpg.font_registry():
        default_font = dpg.add_font("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/Fonts/ProductSans-Regular.ttf", 15)
        second_font = dpg.add_font("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/Fonts/ProductSans-Bold.ttf", 20)
    dpg.bind_font(default_font)
    # ################################################################################################

    # ######################## VARIABLES #########################
    active_fires = []
    exit_list = []
    graph = dij.build_graph(t.read_json(graph_file_path))  # build graph from .json filename
    dij.set_nearest_exit(graph, exit_array)  # run dijkstra and calculate all distances and paths
    # #############################################################
    # ###########################-------------   TEXTURES  -------------##############################

    width, height, channels, data = dpg.load_image(plant_path)
    width1, height1, channels1, data1 = dpg.load_image('/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/esfera.png')
    width2, height2, channels2, data2 = dpg.load_image('/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/fire.png')

    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="image_id")
        dpg.add_static_texture(width1, height1, data1, tag="sphere")
        dpg.add_static_texture(width2, height2, data2, tag="fire")

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





    # ##############################################################################################