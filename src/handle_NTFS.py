from paritioninfowindow import Ui_Partion_Window
from PySide6 import QtCore, QtWidgets
from NTFS import NTFS

class PartitionWindow(QtWidgets.QWidget):
  volume_letter = ""
  root:any
  volume_instance:any
  def __init__(self):
    super().__init__()
    self.ui = Ui_Partion_Window()
    self.ui.setupUi(self)

  def backend_init(self, drive_letter):
    self.volume_letter = drive_letter
    with open ('\\\\.\\' + drive_letter, 'rb') as f:
      self.volume_instance = NTFS(f)
      self.root = self.volume_instance.getDirectoryTree()
    dictionary1 = self.volume_instance.getInfo(get_vbr_info_only=False)
    dictionary2 = self.root.getInfo()
    partion_info_text:str = f'Name: {dictionary2['name']}\n'
    for (key, value) in dictionary1.items():
      partion_info_text += f'{key}: {value}\n'
    self.ui.lb_partionInfo.setText(partion_info_text)

  
