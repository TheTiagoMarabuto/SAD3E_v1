import dearpygui.dearpygui as dpg
from screeninfo import get_monitors
from import_window import *
import os
from new_window import *
help_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."



def show_start_window():
    dpg.create_context()

    plant_path = []
    graph_path = []
    # ###########################-------------   FONT ASSIGNMENT  -------------########################
    with dpg.font_registry():
        default_font = dpg.add_font("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/Fonts/ProductSans-Regular.ttf", 15)
    dpg.bind_font(default_font)

    # ################################################################################################
    # ###########################-------------   TEXTURES  -------------##############################
    width, height, channels, data = dpg.load_image("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/nibble.png")
    width1, height1, channels1, data1 = dpg.load_image("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/feup_logo.png")

    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="nibble_texture")
        dpg.add_static_texture(width1, height1, data1, tag="feup_texture")

    # ##############################################################################################
    # ###########################-------------   FUNCTIONS  -------------############################

    def _config(sender, app_data):

        global plant_path
        global graph_path
        if sender == "new_project_button" or sender == "import_project_button":
            a=5
        if sender == "plant_file_selector":
            plant_path = app_data.get("file_path_name")
            show_new_window(plant_path)
            #print(plant_path)
            #dpg.configure_item("graph_file_selector", show=True)
        if sender == "graph_file_selector":
            graph_path = app_data.get("file_path_name")
            print(graph_path)
            show_import_window(graph_path, plant_path, ["U", "S"])

    # ##############################################################################################
    # ###########################-------------   START WINDOW  -------------############################
    with dpg.window(label="SAD3E", width=500, height=400, no_collapse=True, min_size=(500,)) as window:
        with dpg.collapsing_header(label="Help", tag="help_header"):
            dpg.add_text(help_text, wrap=500)
        with dpg.collapsing_header(label="SAD3E", tag="SA3E_header", default_open=True):
            with dpg.group(horizontal=True):
                dpg.add_button(tag="new_project_button", label="New Project", indent=40, width=200, callback=lambda: dpg.configure_item("plant_file_selector", show=True))
                dpg.add_button(tag="import_project_button", label="Import Project", width=200, callback=lambda: dpg.configure_item("plant_file_selector", show=True))
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                dpg.add_image("feup_texture", tag="feup_logo", width=200)
                dpg.add_image("nibble_texture", tag="nibble_logo", width=200)

    # ##############################################################################################
    with dpg.file_dialog(label="Choose Plant image file", tag="plant_file_selector", show=False, callback=_config, width=500, height=500):
        dpg.add_file_extension("JPG(.jpg){.jpg}", color=(255, 255, 0, 255))
        dpg.add_file_extension("PNG(.png){.png}", color=(0, 255, 0, 255))

    with dpg.file_dialog(label="Choose Graph file", tag="graph_file_selector", show=False, callback=_config, width=500, height=500):
        dpg.add_file_extension("JSON(.json){.json}", color=(255, 255, 0, 255))

