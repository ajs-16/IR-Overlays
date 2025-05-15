import dearpygui.dearpygui as dpg

def create_window():
    with dpg.window(label="Overlay Menu", width=600, height=200, tag="Overlay Menu"):
        dpg.add_text("Select Overlays")
