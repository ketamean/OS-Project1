import sys
import wmi
from PySide6 import QtWidgets, QtCore
from mainwindow import Ui_MainWindow

import LowLevel

from handle import PartitionWindow

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.lb_appFeatures.setText("Sau đây là bảng tính năng của hệ thống:\n1. Chọn thiết bị truy suất\n2. Truy xuất toàn bộ cây thư mục thiết bị\n3. Đọc thông tin ổ truy suất\n4. Thông tin tập tin\n5. Đọc file .txt")
    self.ui.list_volume.itemClicked.connect(self.handle_item_clicked)

  def add_drive(self, text):
    new_item = QtWidgets.QListWidgetItem(text)
    new_item.setTextAlignment(QtCore.Qt.AlignCenter)
    self.ui.list_volume.addItem(new_item)
    
  @QtCore.Slot()
  def handle_item_clicked(self, item):
    partition_type = get_partition_type(item.text())
    self.info = PartitionWindow()
    self.info.backend_init(item.text()[-3:-1], partition_type)
    self.info.show()

def get_partition_type(drive_name):
  drive_letter = drive_name[-3:-1]
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
    window.add_drive(f'{drive.VolumeName if drive.VolumeName != "" else "Logical Disk"} ({drive.Name})')

  window.show()
  sys.exit(app.exec())