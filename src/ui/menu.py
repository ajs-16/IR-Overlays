import dearpygui.dearpygui as dpg
from overlays import input_telemetry

def toggle_overlay(_, app_data, user_data):
    if app_data:
        user_data["open"]()
    else:
        user_data["close"]()

def create_window():
    with dpg.window(label="Overlay Menu", width=600, height=200, tag="Overlay Menu"):
        dpg.add_text("Select Overlays")
        dpg.add_separator()

        # Input Telemetry
        dpg.add_checkbox(
            label="Input Telemetry",
            tag="input_telemetry",
            callback=toggle_overlay,
            user_data={
                    "open": input_telemetry.create_window,
                    "close": input_telemetry.close_window
                }
        )

        dpg.add_checkbox(label="Laptimes", tag="laptimes")
        dpg.add_checkbox(label="Laptime Delta", tag="laptime_delta")
        dpg.add_checkbox(label="Standings", tag="standings")
        dpg.add_checkbox(label="Relatives", tag="Relatives")
