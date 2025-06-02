from PySide6.QtWidgets import QApplication
from ui import menu
import ctypes

if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('iroverlays.iro.1')

    app = QApplication([])
    menuWindow = menu.MainWindow()
    menuWindow.show()
    app.exec()
