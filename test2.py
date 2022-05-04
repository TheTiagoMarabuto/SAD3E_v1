import dearpygui.dearpygui as dpg

from tools import *
from dijkstra import *

graph = build_graph(read_json("/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/edges.json"))
exit_array = ["U", "S"]
set_nearest_exit(graph, exit_array)

x_nodes = []
y_nodes = []

for node in graph:
    x_nodes.append(graph[node].location[0])
    y_nodes.append(graph[node].location[1])

WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
GOLD = (255, 215, 0)
seen_nodes = []
node_label = defaultdict()
edge_label = defaultdict()
dpg.create_context()


width, height, channels, data = dpg.load_image(
    '/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/feup_planta_900.png')
width1, height1, channels1, data1 = dpg.load_image('/Users/tiagomarabuto/PycharmProjects/SAD3E_v1/images/esfera.png')

with dpg.texture_registry():
    dpg.add_static_texture(width, height, data, tag="image_id")
    dpg.add_static_texture(width1, height1, data1, tag="esfera")

with dpg.window(label="Tutorial", width=1200, height=800):
    with dpg.table(header_row=False, no_host_extendX=True, delay_search=True,
                            borders_innerH=True, borders_outerH=True, borders_innerV=True,
                            borders_outerV=True, context_menu_in_body=True, row_background=True,
                            policy=dpg.mvTable_SizingFixedFit, width=200, height=800, scrollY=True):
        dpg.add_table_column(width=200)
        for node in graph:
            with dpg.table_row():
                dpg.add_text("Node: " + node + "->" + graph[node].next_node + "\ndistance to exit: " +
                             str(graph[node].distance_to_exit) + "(" + graph[node].exit + ")")

    with dpg.plot(label="Image Plot", height=800, width=1000, pos=(200,)):
        dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, no_tick_labels=True, no_tick_marks=True)
        with dpg.plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_labels=True, no_tick_marks=True):
            dpg.add_image_series("image_id", [0, 0], [1000, 800])
            for node in graph:
                for dst, weight, hazard in graph[node].edges:
                    # Check if edge was already drew
                    if dst not in seen_nodes:
                        dpg.add_line_series((graph[node].location[0], graph[dst].location[0]),
                                            (graph[node].location[1], graph[dst].location[1]))
            for node in graph:
                dpg.add_image_series("esfera", (graph[node].location[0] - 10, graph[node].location[1] - 10),
                                     (graph[node].location[0] + 10, graph[node].location[1] + 10),
                                     tag=node + "_image")  # label=node+"_image") Uncomment to add ability to hide nodes

        for node in graph:
            dpg.add_plot_annotation(label=node, default_value=3 * graph[node].location[:2], offset=(0, 0),
                                    color=[255, 0, 255])
#with dpg.window(label="Next Nodes", height=800, pos=(1000,0)):


    #dpg.add_text("Next Node:\n", pos=(1000,))
    #for node in graph:
     #   dpg.add_text("\n"+node+"->"+graph[node].next_node+"\ndistance to exit: "+str(graph[node].distance_to_exit)+"("+
      #               graph[node].exit+")", bullet=True, pos=(1000,))

dpg.create_viewport(title='Custom Title', width=1200, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
