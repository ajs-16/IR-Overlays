import dearpygui.dearpygui as dpg
from ui import menu

if __name__ == "__main__":
    dpg.create_context()

    dpg.create_viewport(title='IR Overlays', width=200, height=400, resizable=False)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    menu.create_window()
    dpg.set_primary_window("Overlay Menu", True)

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
