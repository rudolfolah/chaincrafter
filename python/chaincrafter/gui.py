import dearpygui.dearpygui as dpg

VIEWPORT_WIDTH = 800
VIEWPORT_HEIGHT = 600

dpg.create_context()


# callback runs when user attempts to connect attributes
def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)


# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    # app_data -> link_id
    dpg.delete_item(app_data)


with dpg.window(
    label="Tutorial", width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT, no_resize=False, no_close=True, no_collapse=True,
    no_title_bar=True, autosize=True, no_move=True, no_background=True
):
    with dpg.node_editor(callback=link_callback, delink_callback=delink_callback):
        with dpg.node(label="Node 1"):
            with dpg.node_attribute(label="Node A1"):
                dpg.add_input_float(label="F1", width=150)

            with dpg.node_attribute(label="Node A2", attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_input_float(label="F2", width=150)

        with dpg.node(label="Node 2"):
            with dpg.node_attribute(label="Node A3"):
                dpg.add_input_float(label="F3", width=200)

            with dpg.node_attribute(label="Node A4", attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_input_float(label="F4", width=200)

dpg.create_viewport(title='chaincrafter', min_width=VIEWPORT_WIDTH, min_height=VIEWPORT_HEIGHT)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
