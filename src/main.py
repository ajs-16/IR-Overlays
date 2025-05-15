from PySide6.QtWidgets import QApplication
from ui import menu

if __name__ == "__main__":
    app = QApplication([])
    menu_window = menu.MainWindow()
    menu_window.show()
    app.exec()
