from paritioninfowindow import Ui_Partion_Window
from PySide6 import QtCore, QtWidgets
from NTFS import NTFS
from FAT32 import FAT32

import OSItem

extensions = {
      "txt": "Text Editor (e.g., Notepad, Sublime Text)",
      "docx": "Word Processor (e.g., Microsoft Word, LibreOffice Writer)",
      "xlsx": "Spreadsheet (e.g., Microsoft Excel, LibreOffice Calc)",
      "pptx": "Presentation Software (e.g., Microsoft PowerPoint, LibreOffice Impress)",
      "pdf": "PDF Reader (e.g., Adobe Acrobat Reader, Foxit Reader)",
      "jpg": "Image Viewer (e.g., Windows Photos, GIMP)",
      "png": "Image Viewer (e.g., Windows Photos, GIMP)",
      "bmp": "Image Viewer (e.g., Windows Photos, GIMP)",
      "gif": "Image Viewer (e.g., Windows Photos, GIMP)",
      "mp3": "Audio Player (e.g., Windows Media Player, VLC media player)",
      "mp4": "Video Player (e.g., Windows Media Player, VLC media player)",
      "avi": "Video Player (e.g., Windows Media Player, VLC media player)",
      "zip": "Archive Tool (e.g., WinRAR, 7-Zip)",
      "rar": "Archive Tool (e.g., WinRAR, 7-Zip)",
  }

class PartitionWindow(QtWidgets.QWidget):
  volume_letter = ""
  root:any
  volume_instance:any
  def __init__(self):
    super().__init__()
    self.ui = Ui_Partion_Window()
    self.ui.setupUi(self)
    self.ui.lb_partionInfo.setWordWrap(True)
    self.ui.tw_directory.itemDoubleClicked.connect(self.handle_item_doubleClicked)
  
  @QtCore.Slot()
  def handle_item_doubleClicked(self, item:QtWidgets.QTreeWidgetItem):
    
    my_osItem: OSItem.OSItem = item.data(0,QtCore.Qt.UserRole)

    lb_info:str = f'File:\t\t\t\t{item.text(0)}\nLast Modified:\t\t\t{my_osItem.latestModificationDay['day']}/{my_osItem.latestModificationDay['month']}/{my_osItem.latestModificationDay['year']}' + (f'\nSize:\t\t\t\t{my_osItem.size}' if isinstance(my_osItem, OSItem.OSFile) else '')
    self.ui.lb_info.setText(lb_info)

    if (isinstance(my_osItem, OSItem.OSFile)):
      if (my_osItem.extension.lower() == "txt"):
        self.ui.lb_partionInfo.setText(my_osItem.data)
      elif my_osItem.extension.lower() in extensions:
        self.ui.lb_partionInfo.setText('This is not a text file.\n You can use other software to open: ' + extensions[my_osItem.extension.lower()])
      else:
        self.ui.lb_partionInfo.setText('This is not a text file. Unknown extension.')


  def backend_init(self, drive_letter, disk_type):
    self.volume_letter = drive_letter
    with open ('\\\\.\\' + drive_letter, 'rb') as f:
      if (disk_type == "NTFS"):
        self.volume_instance = NTFS(f)
      else:
        self.volume_instance = FAT32(f)
      self.root = self.volume_instance.getDirectoryTree()      
    dictionary1 = self.volume_instance.getInfo(get_vbr_info_only=False)
    dictionary2 = self.root.getInfo()
    partion_info_text:str = f'Name: {dictionary2['name']}\n'
    for (key, value) in dictionary1.items():
      partion_info_text += f'{key}: {value}\n'
    self.ui.lb_partionInfo.setText(partion_info_text)
    self.add_osItem_to_tree(my_osItem=self.root)

  def add_osItem_to_tree(self, my_osItem: OSItem.OSItem, parent_item:QtWidgets.QTreeWidgetItem=None):
    filename = my_osItem.name
    if (isinstance(my_osItem, OSItem.OSFile)):
      filename += '.' + my_osItem.extension
    item = QtWidgets.QTreeWidgetItem([filename])
    item.setData(0, QtCore.Qt.UserRole, my_osItem)
    item.setForeground(0, QtCore.Qt.GlobalColor.white)
    if parent_item:
      parent_item.addChild(item)
    else:
      self.ui.tw_directory.addTopLevelItem(item)
    if (isinstance(my_osItem, OSItem.OSFile)):
      return
    for child in my_osItem.children:
      self.add_osItem_to_tree(my_osItem=child, parent_item=item)
