from AbstractVolume import AbstractVolume
from FAT32 import *
class Navigator:
    """
        class này là interface để GUI gọi và thực hiện các chức năng của chương trình

        class này không thể tạo instance
    """
    _currently_chosen_OSItem    = None       # giữ OSItem (folder hoặc file) đang được chọn
    _current_partition          = None       # giữ partition object hiện đang làm việc

    @staticmethod
    def selectVolume():
        pass

    @staticmethod
    def chooseAppReadFile():
        pass
    
    @staticmethod
    def resetInfo():
        """
            reset các thông tin class này đang giữ
        """
        Navigator._current_partition = None
        Navigator._currently_chosen_OSItem = None


    