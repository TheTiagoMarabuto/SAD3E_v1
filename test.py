import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from import_window import*

dpg.create_context()


#demo.show_demo()
show_import_window("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/edges.json", '/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/feup_planta_900.png', ["U", "S"])

dpg.create_viewport(title='SAD3E', width=1200, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()