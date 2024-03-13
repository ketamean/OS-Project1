"""
    các class dưới đây là để tạo các loại object File và Folder
    
    sử dụng design pattern Composite
"""

class OSItem(object):
    """ các properties của class này
    name                    = ''    # [str] tên file
    status                  = ''    # [str] trạng thái (A/D/V/S/H/R)
                                    # A: archive, D: directory, V: vol lable, S: system, H: hidden, R: read only
    createdTime             = {     # [dict] giờ tạo
        'millisecond': 0,
        'second': 0,
        'minute': 0,
        'hour': 0,
    }
    createdDate             = {     # [dict] ngày tạo
        'day': 0,
        'month': 0,
        'year': 0,
    }
    latestAccessDay         = {     # [dict] ngày truy cập gần nhất
        'day': 0,
        'month': 0,
        'year': 0,
    }
    latestModificationDay   = {     # [dict] ngày truy cập gần nhất
        'day': 0,
        'month': 0,
        'year': 0,
    }
    idxStartingCluster      = 0     # [int] cluster bắt đầu
    size                    = 0     # [int] kích thước
    """
    def __init__(self, name: str, status: str, createdTime_hour: int, createdTime_minute: int, createdTime_second: int, createdTime_millisecond: int, createdDate_day: int, createdDate_month: int, createdDate_year: int, latestAccessDay_day: int, latestAccessDay_month: int, latestAccessDay_year: int, latestModificationDay_day: int, latestModificationDay_month:int, latestModificationDay_year: int, idxStartingCluster: int, size: int) -> None:
        if not (
            isinstance(name, str)                           and
            isinstance(status, str)                         and
            isinstance(createdTime_hour, int)               and
            isinstance(createdTime_minute, int)             and
            isinstance(createdTime_second, int)             and
            isinstance(createdTime_millisecond, int)        and
            isinstance(createdDate_day, int)                and
            isinstance(createdDate_month, int)              and
            isinstance(createdDate_year, int)               and
            isinstance(latestAccessDay_day, int)            and
            isinstance(latestAccessDay_month, int)          and
            isinstance(latestAccessDay_year, int)           and
            isinstance(latestModificationDay_day, int)      and
            isinstance(latestModificationDay_month, int)    and
            isinstance(latestModificationDay_year, int)     and
            isinstance(idxStartingCluster, int)             and
            isinstance(size, int)
        ):
            raise TypeError("Cannot init OSItem: Wrong data type of parameters")
        self.name                           = name
        self.status                         = status

        self.createdTime                    = {}
        self.createdTime['millisecond']     = createdTime_millisecond
        self.createdTime['second']          = createdTime_second
        self.createdTime['minute']          = createdTime_minute
        self.createdTime['hour']            = createdTime_hour

        self.createdDate                    = {}
        self.createdDate['day']             = createdDate_day
        self.createdDate['month']           = createdDate_month
        self.createdDate['year']            = createdDate_year

        self.latestAccessDay                = {}
        self.latestAccessDay['day']         = latestAccessDay_day
        self.latestAccessDay['month']       = latestAccessDay_month
        self.latestAccessDay['year']        = latestAccessDay_year

        self.latestModificationDay          = {}
        self.latestModificationDay['day']   = latestModificationDay_day
        self.latestModificationDay['month'] = latestModificationDay_month
        self.latestModificationDay['year']  = latestModificationDay_year

        self.idxStartingCluster             = idxStartingCluster
        self.size                           = size

    @staticmethod
    def __convertSizeFromBytes(sz):
        order = ['B', 'KB', 'MB', 'GB']
        cnt_order = 0
        while cnt_order < len(order):
            if sz <= 1024:
                break
            print(sz, order[cnt_order])
            sz = sz / 1024
            cnt_order += 1
        return str(sz) + ' ' + (order[cnt_order] if cnt_order < len(order) else order[cnt_order - 1])
    def getInfo(self):
        """
            trả về toàn bộ thông tin của object
        """
        return {
            'Name'                      : self.name,
            'Status'                    : self.status,
            'Created time'              : str(self.createdTime['hour']) + ':' + str(self.createdTime['minute']) + ':' + str(self.createdTime['second']) + '.' + str(self.createdTime['millisecond']) + ', ' + str(self.createdDate['day']) + '/' + str(self.createdDate['month']) + '/' + str(self.createdDate['year']) + ' (dd/mm/yyyy)',
            'Latest access time'        : str(self.latestAccessDay['day']) + '/' + str(self.latestAccessDay['month']) + '/' + str(self.latestAccessDay['year']) + ' (dd/mm/yyyy)',
            'Latest modification time'  : str(self.latestModificationDay['day']) + '/' + str(self.latestModificationDay['month']) + '/' + str(self.latestModificationDay['year']) + ' (dd/mm/yyyy)',
            'Starting cluster'          : str(self.idxStartingCluster),
            'Size'                      : OSItem.__convertSizeFromBytes(self.size),
        }

    def access(self):
        """
            abstract method

            hàm này dùng để `Mở` một item
        """
        raise NotImplementedError

class OSFile(OSItem):
    """ ngoài các properties kế thừa từ parent class, class OSFile còn có thêm các properties
    
    extension       = ''      # [str] phần mở rộng của tập tin
    data            = ''      # [str] nội dung tập tin nếu phần mở rộng là .txt
    """
    def __init__(self, name: str, extension: str, status: str, createdTime_hour: int, createdTime_minute: int, createdTime_second: int, createdTime_millisecond: int, createdDate_day: int, createdDate_month: int, createdDate_year: int, latestAccessDay_day: int, latestAccessDay_month: int, latestAccessDay_year: int, latestModificationDay_day: int, latestModificationDay_month: int, latestModificationDay_year: int, idxStartingCluster: int, size: int, data: str) -> None:
        if not isinstance(extension, str):
            raise TypeError("Cannot init OSFile: Wrong data type of parameters")
        self.extension = extension
        self.data      = data
        super().__init__(name, status, createdTime_hour, createdTime_minute, createdTime_second, createdTime_millisecond, createdDate_day, createdDate_month, createdDate_year, latestAccessDay_day, latestAccessDay_month, latestAccessDay_year, latestModificationDay_day, latestModificationDay_month, latestModificationDay_year, idxStartingCluster, size)
    
    def access(self):
        pass

    def getInfo(self):
        res = super().getInfo()
        res['Name'] = self.name + '.' + self.extension
        return res

class OSFolder(OSItem):
    """ ngoài các properties kế thừa từ parent class, class OSFolder còn có thêm các properties

    children = []               # [list] danh sách các OSFile và OSFolder con trong một OSFolder lớn hơn
    """
    def __init__(self, name: str, status: str, createdTime_hour: int, createdTime_minute: int, createdTime_second: int, createdTime_millisecond: int, createdDate_day: int, createdDate_month: int, createdDate_year: int, latestAccessDay_day: int, latestAccessDay_month: int, latestAccessDay_year: int, latestModificationDay_day: int, latestModificationDay_month: int, latestModificationDay_year: int, idxStartingCluster: int, size: int) -> None:
        self.children = []
        super().__init__(name, status, createdTime_hour, createdTime_minute, createdTime_second, createdTime_millisecond, createdDate_day, createdDate_month, createdDate_year, latestAccessDay_day, latestAccessDay_month, latestAccessDay_year, latestModificationDay_day, latestModificationDay_month, latestModificationDay_year, idxStartingCluster, size)    
    
    def addChild(self, ositem: OSItem):
        self.children.append(ositem)
    
    def access(self):
        pass
    
    def getInfo(self):
        res = super().getInfo()
        res['Size'] = '-'
        return res

if __name__ == '__main__':
    # test initializers
    print('Testing...')
    file = OSFile('file_nek','.txt','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    folder = OSFolder('DIR','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    print("file: ", file.getInfo())
    folder.addChild(file)
    folder.access()
    print('\nTested')