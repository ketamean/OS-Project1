import sys
import wmi
from PySide6 import QtWidgets, QtCore
from mainwindow import Ui_MainWindow

import LowLevel

from handle_NTFS import PartitionWindow

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.list_volume.itemClicked.connect(self.handle_item_clicked)

  def add_drive(self, text):
    new_item = QtWidgets.QListWidgetItem(text)
    new_item.setTextAlignment(QtCore.Qt.AlignCenter)
    self.ui.list_volume.addItem(new_item)
    
  @QtCore.Slot()
  def handle_item_clicked(self, item):
    partition_type = get_partition_type(item.text())
    if partition_type == "NTFS":
      self.info = PartitionWindow()
      self.info.backend_init(item.text())
      self.info.show()

def get_partition_type(drive_letter):
  with open ('\\\\.\\' + drive_letter, 'rb') as f:
    sector = LowLevel.readSector(fileobject=f, nsector=1)
    fat32_type = sector[0x52:0x52 + 8]
    if (b'FAT32' in fat32_type):
      print("FAT32 detected")
      return "FAT32"
    else:
      print("NTFS detected")
      return "NTFS"



if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  window = MainWindow()

  drives = wmi.WMI().Win32_LogicalDisk()
  
  for drive in drives:
    window.add_drive(drive.Name)

  window.show()
  sys.exit(app.exec())