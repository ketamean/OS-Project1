from paritioninfowindow import Ui_Partion_Window
from PySide6 import QtCore, QtWidgets
from NTFS import NTFS

class PartitionWindow(QtWidgets.QWidget):
  volume_letter = ""
  root:any
  def __init__(self):
    super().__init__()
    self.ui = Ui_Partion_Window()
    self.ui.setupUi(self)

  def backend_init(self, drive_letter):
    self.volume_letter = drive_letter
    with open ('\\\\.\\' + drive_letter, 'rb') as f:
      tmp = NTFS(f)
      self.root = tmp.getDirectoryTree()
    dictionary = self.root.getInfo()
    print(type(dictionary))
    self.ui.lb_partionInfo.setText(f'Name: {dictionary['name']}')

  
