import sys

from PySide6 import QtWidgets, QtCore
from mainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec())