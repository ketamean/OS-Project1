from paritioninfowindow import Ui_Partion_Window
from PySide6 import QtCore, QtWidgets
from NTFS import NTFS
import OSItem
class PartitionWindow(QtWidgets.QWidget):
  volume_letter = ""
  root:any
  volume_instance:any
  def __init__(self):
    super().__init__()
    self.ui = Ui_Partion_Window()
    self.ui.setupUi(self)
    self.ui.tw_directory.itemDoubleClicked.connect(self.handle_item_doubleClicked)
  
  @QtCore.Slot()
  def handle_item_doubleClicked(self, item:QtWidgets.QTreeWidgetItem):
    self.ui.lb_info.setText(item.text(0))
    my_osItem: OSItem.OSItem = item.data(0,QtCore.Qt.UserRole)
    if (isinstance(my_osItem, OSItem.OSFile)):
      if (my_osItem.extension == "txt"):
        self.ui.lb_partionInfo.setText(my_osItem.data)
      else:
        self.ui.lb_partionInfo.setText('This is not a text file')

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
