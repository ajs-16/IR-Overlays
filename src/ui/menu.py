import dearpygui.dearpygui as dpg

def create_window():
    with dpg.window(label="Overlay Menu", width=600, height=200, tag="Overlay Menu"):
        dpg.add_text("Select Overlays")
        dpg.add_separator()
        dpg.add_checkbox(label="Input Telemetry", tag="input_telemetry")
        dpg.add_checkbox(label="Laptimes", tag="laptimes")
        dpg.add_checkbox(label="Laptime Delta", tag="laptime_delta")
        dpg.add_checkbox(label="Standings", tag="standings")
        dpg.add_checkbox(label="Relatives", tag="Relatives")
