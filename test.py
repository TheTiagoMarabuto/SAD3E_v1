import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from import_window_v1 import*
from start_window import *
from new_window import*
dpg.create_context()

#show_start_window()
demo.show_demo()
#show_import_window("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/edges.json", '/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/feup_planta_900.png')
#show_new_window('/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/Presentation1.jpg')
dpg.create_viewport(title='SAD3E')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()