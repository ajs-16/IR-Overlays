import dearpygui.dearpygui as dpg

def create_window():
    with dpg.window(
        label="Input Telemetry Overlay",
        width=100,
        height=100,
        tag="input_telemetry_overlay",
        no_background=True,
        no_resize=True,
        no_close=True,
        no_scrollbar=True,
        no_title_bar=True
    ):
        dpg.add_text("Input Telemetry Overlay")

def close_window():
    dpg.delete_item("input_telemetry_overlay", children_only=True)
    dpg.delete_item("input_telemetry_overlay")
