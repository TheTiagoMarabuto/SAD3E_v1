import dearpygui.dearpygui as dpg
from screeninfo import get_monitors
from import_window import *
from new_window import *
help_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

screen_height = get_monitors()[0].height
screen_width = get_monitors()[0].width

screen_middle = (screen_width / 2, screen_height / 2)

def new_button_action(sender, data):
    a=0

def import_button_action(sender, data):
    #dpg.create_viewport(title="SAD3E - Run",width=screen_width, height=screen_height)
    with dpg.window(label="SAD3E - Run", width=screen_width, height=screen_height) as sad3e_run:
        menu_bar = dpg.add_menu_bar()
        dpg.show_viewport(maximized=True)

dpg.create_context()
dpg.create_viewport(title="SAD3E", width=500, height=400, x_pos=390, y_pos=250)


with dpg.window(label="SAD3E", width=500, height=400, no_move=True, no_collapse=True, min_size=(500, ), no_close=True,
                no_resize=True) as window:

    help_page = dpg.add_collapsing_header(label="Help")
    dpg.add_text(help_text, parent=help_page, wrap=500)

    button_page = dpg.add_collapsing_header(label="SAD3E", default_open=True,)
    button_group = dpg.add_group(horizontal=True, parent=button_page)
    dpg.add_button(label="New Project", parent=button_group, indent=40, width=200)
    dpg.add_button(label="Import Project", parent=button_group, width=200, callback=import_button_action)

    width, height, channels, data = dpg.load_image("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/nibble.png")

    with dpg.texture_registry():
        texture_id = dpg.add_static_texture(width, height, data)
    dpg.add_image(texture_id, parent=window, pos=(250 - width / 2, 350 - height))

    width1, height1, channels1, data1 = dpg.load_image(
        "/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/feup_logo.png")

    with dpg.texture_registry():
        texture_id = dpg.add_static_texture(width1, height1, data1)
    dpg.add_image(texture_id, parent=window, pos=(250 - width1 / 2, 350 - height - height1))


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
