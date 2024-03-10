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

    def getInfo(self):
        """
            trả về toàn bộ thông tin của object
        """
        return {
            'name'                  : self.name,
            'status'                : self.status,
            'createdTime'           : self.createdTime,
            'createdDate'           : self.createdDate,
            'createdDate'           : self.latestAccessDay,
            'latestModificationDay' : self.latestModificationDay,
            'idxStartingCluster'    : self.idxStartingCluster,
            'size'                  : self.size,
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
    """
    def __init__(self, name: str, extension: str, status: str, createdTime_hour: int, createdTime_minute: int, createdTime_second: int, createdTime_millisecond: int, createdDate_day: int, createdDate_month: int, createdDate_year: int, latestAccessDay_day: int, latestAccessDay_month: int, latestAccessDay_year: int, latestModificationDay_day: int, latestModificationDay_month: int, latestModificationDay_year: int, idxStartingCluster: int, size: int) -> None:
        if not isinstance(extension, str):
            raise TypeError("Cannot init OSFile: Wrong data type of parameters")
        self.extension = extension
        super().__init__(name, status, createdTime_hour, createdTime_minute, createdTime_second, createdTime_millisecond, createdDate_day, createdDate_month, createdDate_year, latestAccessDay_day, latestAccessDay_month, latestAccessDay_year, latestModificationDay_day, latestModificationDay_month, latestModificationDay_year, idxStartingCluster, size)
    
    def access(self, lvl):
        # # these following commented lines are for testing
        # print('open file: ', self.name, end='')
        tab = ''
        for i in range(lvl):
            tab += '\t' 
        print(tab + self.name)
        pass

    def getInfo(self):
        res = super().getInfo()
        res['extension'] = self.extension
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
    
    def access(self, lvl):
        # # these following commented lines are for testing
        # print('open folder: ', self.name, ', contains: [', end='')
        # for i in self.children:
        #     i.access()
        #     print(',', end='')
        # print(']',end='')
        tab = ''
        for i in range(lvl):
            tab += '\t' 
        print(tab + self.name)
        for child in self.children:
            child.access(lvl + 1)
        pass

if __name__ == '__main__':
    # test initializers
    print('Testing...')
    file = OSFile('file_nek','.txt','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    folder = OSFolder('DIR','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    print("file: ", file.getInfo())
    folder.addChild(file)
    folder.access()
    print('\nTested')