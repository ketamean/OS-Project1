import os
from AbstractVolume import *
from LowLevel import *
from OSItem import *

class FAT32(AbstractVolume):
    """ ngoài các properties kế thừa từ parent class, class FAT32 còn có thêm các properties
    
    nFatTable               = 0         # [int] số bảng FAT
    sizeFatTable            = 0         # [int] kích thước mỗi bảng FAT
    rdetStartCluster        = 0         # [int] chỉ số cluster bắt đầu của RDET
    
    """
    # Override các abstract attribute 
    root_directory = None 
    size = None
    volume_label = None 
    file_object = None

    __root_osfolder = None

    def __init__(self, file_object) -> None:
        self.file_object = file_object
        # Khởi tạo các properties của class
        self.nFatTable = 0              # [int] số bảng FAT
        self.sizeFatTable = 0           # [int] kích thước mỗi bảng FAT
        self.rdetStartCluster = 0       # [int] chỉ số cluster bắt đầu của RDET
        self.dataStartSector = 0        # [int] sector bắt đầu của vùng dữ liệu

        # Đọc thông tin từ boot sector để set properties    
        buffer = readSector(file_object, 1)

        # [int] số byte trên sector, đọc từ offset 11 tới 12
        self.nBytesPerSector = int.from_bytes(buffer[11:13], byteorder='little') 
        # [int] số sector trên cluster, đọc từ offset 13, 1 offset
        self.nSectorsPerCluster = int.from_bytes(buffer[13:14], byteorder='little')
        # [int] số sector trên bootsector, đọc từ offset 14, 2 offset
        self.nSectorsOnBootSector = int.from_bytes(buffer[14:16], byteorder='little')
        # [int] số sector trên đĩa, đọc từ offset 24, 2 offset
        self.nSectorPerTrack = int.from_bytes(buffer[24:26], byteorder='little')
        # [int] số đầu đọc trên đĩa, đọc từ offset 26, 2 offset
        self.nHead = int.from_bytes(buffer[26:28], byteorder='little')
        # [int] số sector của volume, đọc từ offset 32, 4 offset
        self.sizeVolume = int.from_bytes(buffer[32:36], byteorder='little')

        # Đọc các thông tin của FAT32
        # [int] số fat table, đọc từ offset 16, 1 offset
        self.nFatTable = int.from_bytes(buffer[16:17], byteorder='little')
        # [int] kích thước mỗi bảng FAT, đọc từ offset 36, 4 offset
        self.sizeFatTable = int.from_bytes(buffer[36:40], byteorder='little')
        # [int] cluster bắt đầu của bảng RDET, đọc từ offset 44, 4 offset
        self.rdetStartCluster = int.from_bytes(buffer[44:48], byteorder='little')
        # [str] partition type, đọc từ offset 82, 8 offset
        self.partitionType = buffer[82:90].decode('utf-8').strip()
        # Sector bắt đầu của vùng dữ liệu: = Sb + Nf * Sf
        self.dataStartSector = self.nSectorsOnBootSector + self.nFatTable * self.sizeFatTable

        # Khởi tạo lại giá trị abstract
        # super().__init__(self.nBytesPerSector, self.nSectorsPerCluster, self.nSectorsOnBootSector, self.nSectorPerTrack, self.nHead, self.sizeVolume, self.partitionType)

        # Đọc bảng FAT (sf byte tại offset sb)
        self.fat_table_buffer = readSector(
            fileobject=self.file_object,
            nsector=self.sizeFatTable * self.nSectorsPerCluster,
            beginSector=self.nSectorsOnBootSector,
            bytePerSector=self.nBytesPerSector
        )

        # RDET buffer
        clusterChain = self.readRDETCluster(self.rdetStartCluster)
        sectorChain = self.clusterToSector(clusterChain)
        RDETbuffer = readSectorBuffer(self.file_object, sectorChain, self.nBytesPerSector)

        self.root_directory = TmpFATDir(RDETbuffer[0:32], '', self, isrdet=True)

        self.__root_osfolder = self.root_directory.get_ositem()
        
    def getInfo(self, get_vbr_info_only = True):
        res = super().getInfo()
        if not get_vbr_info_only:
            res['Number of FAT'] = str(self.nFatTable) + ' table' + ('s' if self.nFatTable >= 2 else '')
            res['Size of each FAT'] = str(self.sizeFatTable) + ' cluster' + ('s' if self.nFatTable >= 2 else '')
            res['Starting cluster of RDET'] = self.rdetStartCluster
            res['Starting cluster of data region'] = self.dataStartSector
        return res
    
    def getDirectoryTree(self):
        return self.__root_osfolder
    
    def readRDETCluster(self, startCluster) -> list:
        """
        Hàm dùng để dò bảng FAT ra dãy cluster của RDET, bắt đầu từ startCluster
        """
        # Kiểm tra cluster hợp lệ
        def isValid(cls_num):
            return (cls_num >= 0x2) and (cls_num <= 0xFFFFFEF)
        
        if not isValid(startCluster):
            return []
        nextCluster = startCluster
        chain = [nextCluster]
        while True:
            # Bảng FAT bỏ 2 phần tử đầu, bắt đầu từ phần tử 2
            nextCluster = int.from_bytes(self.fat_table_buffer[nextCluster * 4:nextCluster * 4 + 4], 'little')
            # readSector(FATbuffer, 4, nextCluster * 4)
            if not isValid(nextCluster):
                break
            else:
                chain.append(nextCluster)

        return chain


    def clusterToSector(self, clusterChain) -> list: 
        """
        Hàm chuyển đổi dãy cluster thành dãy sector
        Ta có 1 cluster có Sc sector -> cluster k  bắt đầu từ beginSector + k * Sc
        Vì FAT32 có RDET nằm trên vùng dữ liệu -> cluster đánh số từ 2
        """
        chain = []
        
        for cluster in clusterChain:
            begin_sector = self.dataStartSector + (cluster - 2) * self.nSectorsPerCluster
            for sector in range(begin_sector, begin_sector + self.nSectorsPerCluster):
                chain.append(sector)
        return chain

    @staticmethod
    def join_lfnentries(subentries: list):
        """
        Hàm join các entry phụ lại thành tên dài
        """
        name = b''
        # nối các dãy đọc từ list các subentry
        for subentry in subentries:
            name += readBuffer(subentry, 1, 10)
            name += readBuffer(subentry, 0xE, 12)
            name += readBuffer(subentry, 0x1C, 4)
        name = name.decode('utf-16le', errors='ignore')

        if name.find('\x00') > 0:
            name = name[:name.find('\x00')]
        return name

class TmpFATDir():
    """
    Lớp đối tượng thể hiện một thư mục trong FAT
    """
    # Override các abstract attribute 
    volume = None
    subentries = None
    name = None
    attr = None
    sectors = None
    path = None
    size = None
    created_day = None
    created_time = None
    modified_day = None
    def get_ositem(self):
        res = OSFolder (
            name=self.name,
            status=self.describe_attr(),
            createdDate_day=self.created_day[2],
            createdDate_month=self.created_day[1],
            createdDate_year=self.created_day[0],
            createdTime_hour=self.created_time[0],
            createdTime_minute=self.created_time[1],
            createdTime_second=self.created_time[2],
            createdTime_millisecond=self.created_time[3],
            latestAccessDay_day=self.latest_access_day[2],
            latestAccessDay_month=self.latest_access_day[1],
            latestAccessDay_year=self.latest_access_day[0],
            latestModificationDay_day=self.modified_day[2],
            latestModificationDay_month=self.modified_day[1],
            latestModificationDay_year=self.modified_day[0],
            idxStartingCluster=self.begin_cluster,
            size=self.size,
        )
        if self.subentries:
            for child in self.subentries:
                res.children.append(child.get_ositem())
        return res
  
    def __init__(self, main_entry_buffer: bytes, parent_path: str, volume: FAT32, isrdet=False, lfn_entries=[]):
        # Dãy byte entry chính
        self.entry_buffer = main_entry_buffer
        self.volume = volume # con trỏ đến volume đang chứa thư mục này
        # Danh sách các subentry
        self.subentries = None

        # Tên entry
        if len(lfn_entries) > 0:
            lfn_entries.reverse()
            self.name = FAT32.join_lfnentries(lfn_entries).upper()
            lfn_entries.clear()
        else:
            self.name = readBuffer(main_entry_buffer, 0, 11).decode('utf-8', errors='ignore').strip().upper()
        # Nếu thư mục này là RDET (file thì ko cần xét RDET)
        if not isrdet:
            # Status
            self.attr = main_entry_buffer[0xB]

            # Các byte thấp và cao của chỉ số cluster đầu
            highbytes = int.from_bytes(bytes=main_entry_buffer[0x14:0x14 + 2], byteorder='little')
            lowbytes = int.from_bytes(bytes=main_entry_buffer[0x1A:0x1A + 2], byteorder='little')
            self.begin_cluster = highbytes * 0x100 + lowbytes
            self.path = parent_path + '/' + self.name
        else:
            self.begin_cluster = self.volume.rdetStartCluster
            self.path = ''

        cluster_chain = self.volume.readRDETCluster(self.begin_cluster)
        self.sectors = self.volume.clusterToSector(cluster_chain)

        # Kích thước tập tin
        self.size = int.from_bytes(main_entry_buffer[0x1C:0x1C + 4], 'little')
        # Extracting created day and time
        created_date = int.from_bytes(main_entry_buffer[0x10:0x10 + 2], 'little')
        created_time = int.from_bytes(main_entry_buffer[0x0D:0x0D + 3], 'little')
        self.created_day, self.created_time = self.decode_datetime(created_date, created_time)

        # Extracting latest modified day
        modified_date = int.from_bytes(main_entry_buffer[0x18:0x18 + 2], 'little')
        self.modified_day = self.decode_date(modified_date)

        access_day = int.from_bytes(main_entry_buffer[0x12:0x12 + 2], 'little')
        self.latest_access_day = self.decode_date(access_day)

        self.build_tree(issdet=not isrdet)

    def decode_datetime(self, date_bytes, time_bytes):
        # convert date
        """
        Hàm decode từ hex ra ngày, tháng, năm và giờ, phút, giây, mili giây
        Nhận vào dãy hex và trả về Dec
        """

        year = ((date_bytes >> 9) & 0x7F) + 1980  # Bits 9–15: Count of years from 1980, valid value range 0–127 inclusive (1980–2107)
        month = (date_bytes >> 5) & 0x0C # Bits 5–8: Month of year, 1 = January, valid value range 1–12 inclusive. 
        day = date_bytes & 0x1F # Bits 0–4: Day of month, valid value range 1-31 inclusive. 

        # convert time
        hour = (time_bytes >> 19) & 0x1F # Bits 19-24: hour, valid value range 0-23 inclusive
        minute = (time_bytes >> 13) & 0x3F # Bits 13-18: minute, valid value range 0-59 inclusive
        second = ((time_bytes >> 7) & 0x3F) # Bits 7–12: 2-second count, valid value range 0–29 inclusive (0 – 58 seconds).
        millisecond = (time_bytes) & 0xC7 # Bits 0-6: milisec, valid range 0-99 inclusive.

        return (year, month, day), (hour, minute, second, millisecond)

    def decode_date(self, date_bytes):
        """
        Hàm decode từ hex ra ngày, tháng, năm
        Làm việc tương tự hàm 'decode_datetime'
        """
        year = ((date_bytes >> 9) & 0x7F) + 1980
        month = (date_bytes >> 5) & 0x0F
        day = date_bytes & 0x1F

        return year, month, day
            
    def build_tree(self, issdet = True):
        """
        Dựng cây thư mục cho thư mục này (đọc các sector trong mảng `self.sectors` được SDET rồi xử lý)
        """
        if self.subentries != None: 
            # Nếu đã dựng rồi thì ko làm lại nữa
            return
        self.subentries = []
        subentry_index = 0

        # Đọc SDET (dữ liệu nhị phân) của thư mục
        sdet_buffer = readSectorBuffer(self.volume.file_object, self.sectors, self.volume.nBytesPerSector)
        lfn_entries_queue = []
        if issdet:
            sdet_buffer = sdet_buffer[64:]
        while True:
            subentry_buffer = readBuffer(sdet_buffer, subentry_index, 32)
            subentry_index += 32
            # Kiểm tra offset đầu của entry
            # check NOT IN USE
            if subentry_buffer[0] == 0xE5:
                continue
            # Read type
            entry_type = subentry_buffer[0xB]
            if entry_type == 0:
                break
            elif entry_type & 0x0F == 0x0F:
                lfn_entries_queue.append(subentry_buffer)
            elif entry_type & 0x20 == 0x20:
                # Là tập tin (archive)
                self.subentries.append(TmpFATFile(subentry_buffer, self.path, self.volume, lfn_entries=lfn_entries_queue))
                lfn_entries_queue = []
            elif entry_type & 0x10 == 0x10:
                # Là thư mục
                self.subentries.append(TmpFATDir(subentry_buffer, self.path, self.volume, lfn_entries=lfn_entries_queue))
                lfn_entries_queue = []

    def print_tree(self, indent=0):
        """
        In cây
        """
        print("  " * indent + self.name + "/")
        if self.subentries:
            for entry in self.subentries:
                if isinstance(entry, TmpFATDir):
                    entry.print_tree(indent + 1)
                else:
                    print("  " * (indent + 1) + entry.name)

    def build_and_print_tree(self):
        """
        Hàm gọi xây cây và in cây
        """
        self.build_tree()
        self.print_tree()

    def describe_attr(self):
        """
        Lấy chuỗi mô tả các thuộc tính
        """
        desc_map = {
            0x10: 'D', # Directory
            0x20: 'A', # Archive
            0x01: 'R', # Read Only
            0x02: 'H', # Hidden
            0x04: 'S', # System
            0x08: 'V', # VolLable
        }
        if not self.attr:
            return ''
        desc_str = ''
        for attribute in desc_map:
            if self.attr & attribute == attribute:
                desc_str += desc_map[attribute]
        
        return desc_str

class TmpFATFile():
    volume = None 
    name = None 
    attr = None 
    sectors = None
    path = None
    size = None
    created_day = None
    created_time = None
    modified_day = None

    def get_ositem(self):
        return OSFile (
            name=self.name_base,
            extension=self.name_ext,
            status=self.describe_attr(),
            createdDate_day=self.created_day[2],
            createdDate_month=self.created_day[1],
            createdDate_year=self.created_day[0],
            createdTime_hour=self.created_time[0],
            createdTime_minute=self.created_time[1],
            createdTime_second=self.created_time[2],
            createdTime_millisecond=self.created_time[3],
            latestAccessDay_day=self.latest_access_day[2],
            latestAccessDay_month=self.latest_access_day[1],
            latestAccessDay_year=self.latest_access_day[0],
            latestModificationDay_day=self.modified_day[2],
            latestModificationDay_month=self.modified_day[1],
            latestModificationDay_year=self.modified_day[0],
            idxStartingCluster=self.begin_cluster,
            size=self.size,
            data=self.data
        )
    
    def __init__(self, main_entry_buffer: bytes, parent_path: str, volume: FAT32, lfn_entries=[]):
        ...
        self.entry_buffer = main_entry_buffer
        self.volume = volume

        # Thuộc tính trạng thái
        self.attr = main_entry_buffer[0xB]

        # Tên entry 
        if len(lfn_entries) > 0:
            lfn_entries.reverse()
            self.name = FAT32.join_lfnentries(lfn_entries)
            lfn_entries.clear()
            if self.name.rfind('.') >= 0:
                self.name_base = self.name[:self.name.rfind('.')].upper()
                self.name_ext = self.name[self.name.rfind('.')+1:].upper()
            else:
                self.name_base = self.name
                self.name_ext = ''
        else:
            self.name_base = readBuffer(main_entry_buffer, 0, 8).decode('utf-8', errors='ignore').strip().upper()
            self.name_ext = readBuffer(main_entry_buffer, 8, 3).decode('ascii', errors='ignore').strip().upper()
            self.name = self.name_base + '.' + self.name_ext

        # Phần Word(2 byte) cao và thấp
        highbytes = int.from_bytes(bytes=main_entry_buffer[0x14:0x14 + 2], byteorder='little')
        lowbytes = int.from_bytes(bytes=main_entry_buffer[0x1A:0x1A + 2], byteorder='little')

        # Cluster bắt đầu
        self.begin_cluster = highbytes * 0x100 + lowbytes

        # Đường dẫn tập tin
        self.path = parent_path + '/' + self.name

        cluster_chain = self.volume.readRDETCluster(self.begin_cluster)

        self.sectors = self.volume.clusterToSector(cluster_chain)

        # Kích thước tập tin
        self.size = int.from_bytes(main_entry_buffer[0x1C:0x1C + 4], 'little')

        # Extracting created day and time
        created_date = int.from_bytes(main_entry_buffer[0x10:0x10 + 2], 'little')
        created_time = int.from_bytes(main_entry_buffer[0x0D:0x0D + 3], 'little')
        self.created_day, self.created_time = self.decode_datetime(created_date, created_time)

        # Extracting latest modified day
        modified_date = int.from_bytes(main_entry_buffer[0x18:0x18 + 2], 'little')
        self.modified_day = self.decode_date(modified_date)

        access_day = int.from_bytes(main_entry_buffer[0x12:0x12 + 2], 'little')
        self.latest_access_day = self.decode_date(access_day)
        self.data = None
        if self.name_ext == 'TXT':
            self.data = self.dump_binary_data().decode('utf-8')
        
    def decode_datetime(self, date_bytes, time_bytes):
        year = ((date_bytes >> 9) & 0x7F) + 1980
        month = (date_bytes >> 5) & 0x0C
        day = date_bytes & 0x1F

        hour = (time_bytes >> 19) & 0x1F
        minute = (time_bytes >> 13) & 0x3F
        second = ((time_bytes >> 7) & 0x3F)
        millisecond = (time_bytes) & 0xC7

        return (year, month, day), (hour, minute, second, millisecond)

    def decode_date(self, date_bytes):
        year = ((date_bytes >> 9) & 0x7F) + 1980
        month = (date_bytes >> 5) & 0x0F
        day = date_bytes & 0x1F

        return year, month, day
    
    def dump_binary_data(self):
        """
        Trả về mảng các byte của tập tin
        """
        binary_data = readSectorBuffer(self.volume.file_object, self.sectors, self.volume.nBytesPerSector)
        # "trim" bớt cho về đúng kích thước
        return binary_data[:self.size]

    def describe_attr(self):
        desc_map = {
            0x10: 'D', # Directory
            0x20: 'A', # Archive
            0x01: 'R', # Read Only
            0x02: 'H', # Hidden
            0x04: 'S', # System
            0x08: 'V', # VolLable
        }

        desc_str = ''
        for attribute in desc_map:
            if self.attr & attribute == attribute:
                desc_str += desc_map[attribute]
        
        return desc_str

if __name__ == '__main__':
    volume_path = input('=> Enter your drive path: ')
    volume_path = '\\\\.\\' + volume_path + ':'
    fd = os.open(volume_path, os.O_RDONLY | os.O_BINARY)
    f = os.fdopen(fd, 'rb')
    fat32_volume = FAT32(f)
    root = fat32_volume.getDirectoryTree()
    root.access(0)
