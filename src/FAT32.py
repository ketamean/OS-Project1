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

    # def __new__(cls):
    #     return super().__new__()
    def __init__(self, file_object) -> None:
        self.file_object = file_object
        # Khởi tạo các properties của class
        self.nFatTable = 0              # [int] số bảng FAT
        self.sizeFatTable = 0           # [int] kích thước mỗi bảng FAT
        self.rdetStartCluster = 0       # [int] chỉ số cluster bắt đầu của RDET
        self.dataStartSector = 0        # [int] sector bắt đầu của vùng dữ liệu

        # Đọc thông tin từ boot sector để set properties    
        buffer = readSector(file_object, 1)
        # print('Boot Sector')
        # print(buffer)
        # print('\n')

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
        super().__init__(self.nBytesPerSector, self.nSectorsPerCluster, self.nSectorsOnBootSector, self.nSectorPerTrack, self.nHead, self.sizeVolume, self.partitionType)

        # Đọc bảng FAT (sf byte tại offset sb)
        self.fat_table_buffer = readSector(self.file_object, 10, self.nSectorsOnBootSector + 1)
        # print('FAT Table')
        # print(self.fat_table_buffer)
        # print('\n')

        # RDET buffer
        clusterChain = self.readRDETCluster(self.rdetStartCluster)
        sectorChain = self.clusterToSector(clusterChain)
        RDETbuffer = read_sector_chain(self.file_object, sectorChain, self.nBytesPerSector)

        self.root_directory = FATDirectory(RDETbuffer, '', self, isrdet=True)
    
    def readRDETCluster(self, startCluster) -> list:
        """
        Hàm dùng để dò bảng FAT ra dãy cluster của RDET, bắt đầu từ startCluster
        """
        # Kiểm tra cluster kết thúc
        eoCluster = [0x00000000, 0xFFFFFF0, 0xFFFFFFF, 0XFFFFFF7, 0xFFFFFF8, 0xFFFFFFF0]
        if startCluster in eoCluster:
            return []
        
        nextCluster = startCluster
        chain = [nextCluster]

        while True:
            # Bảng FAT bỏ 2 phần tử đầu, bắt đầu từ 0 -> phần tử 2 = cluster 1
            nextCluster = read_number_buffer(self.fat_table_buffer, nextCluster * 4, 4)
            # readSector(FATbuffer, 4, nextCluster * 4)
            if nextCluster in eoCluster:
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
    def process_fat_lfnentries(subentries: list):
        """
        Hàm join các entry phụ lại thành tên dài
        """
        name = b''
        for subentry in subentries:
            name += read_bytes_buffer(subentry, 1, 10)
            name += read_bytes_buffer(subentry, 0xE, 12)
            name += read_bytes_buffer(subentry, 0x1C, 4)
        name = name.decode('utf-16le', errors='ignore')

        if name.find('\x00') > 0:
            name = name[:name.find('\x00')]
        return name
    
    def initialize_root_directory(self, file_object):
        """
        Tạo một thể hiện cụ thể của AbstractDrive từ tham chiếu file nhận được.
        Dựng cây thư mục gốc
        """
        self.volume = FAT32(file_object)
        print(self.volume.getInfo())
        print('\n')
        self.volume.root_directory.build_tree()
        self.current_dir = self.volume.root_directory

    def generate_table_view(self):
        entry_info_list = []
        max_width = {}

        def update_max_width(key, value):
            if key not in max_width:
                max_width[key] = len(str(value)) + 4
            elif max_width[key] < len(str(value)):
                max_width[key] = len(str(value)) + 4

        for entry in self.current_dir.subentries:
            entry_info = {
                'name': entry.name,
                'status': 'Directory' if isinstance(entry, AbstractDirectory) else 'File',
                'createdTime_hour': entry.created_time[0] if hasattr(entry, 'created_time') else '-',
                'createdTime_minute': entry.created_time[1] if hasattr(entry, 'created_time') else '-',
                'createdTime_second': entry.created_time[2] if hasattr(entry, 'created_time') else '-',
                'createdTime_millisecond': entry.created_time[3] if hasattr(entry, 'created_time') else '-',
                'createdDate_day': entry.created_day[2] if hasattr(entry, 'created_day') else '-',
                'createdDate_month': entry.created_day[1] if hasattr(entry, 'created_day') else '-',
                'createdDate_year': entry.created_day[0] if hasattr(entry, 'created_day') else '-',
                'latestAccessDay_day': entry.latest_access_day[2] if hasattr(entry, 'latest_access_day') else '-',
                'latestAccessDay_month': entry.latest_access_day[1] if hasattr(entry, 'latest_access_day') else '-',
                'latestAccessDay_year': entry.latest_access_day[0] if hasattr(entry, 'latest_access_day') else '-',
                'latestModificationDay_day': entry.modified_day[2] if hasattr(entry, 'modified_day') else '-',
                'latestModificationDay_month': entry.modified_day[1] if hasattr(entry, 'modified_day') else '-',
                'latestModificationDay_year': entry.modified_day[0] if hasattr(entry, 'modified_day') else '-',
                'beginCluster': entry.begin_cluster if hasattr(entry, 'begin_cluster') else '-'
            }
            if entry_info['name'] in ('.', '..'):
                continue

            entry_info_list.append(entry_info)

            for key, value in entry_info.items():
                update_max_width(key, value)

        format_str = '{{name: <{name_width}}} {{status: <{status_width}}} {{createdTime_hour: <{createdTime_hour_width}}} ' \
                    '{{createdTime_minute: <{createdTime_minute_width}}} {{createdTime_second: <{createdTime_second_width}}} ' \
                    '{{createdTime_millisecond: <{createdTime_millisecond_width}}} {{createdDate_day: <{createdDate_day_width}}} ' \
                    '{{createdDate_month: <{createdDate_month_width}}} {{createdDate_year: <{createdDate_year_width}}} ' \
                    '{{latestAccessDay_day: <{latestAccessDay_day_width}}} {{latestAccessDay_month: <{latestAccessDay_month_width}}} ' \
                    '{{latestAccessDay_year: <{latestAccessDay_year_width}}} {{latestModificationDay_day: <{latestModificationDay_day_width}}} ' \
                    '{{latestModificationDay_month: <{latestModificationDay_month_width}}} {{latestModificationDay_year: <{latestModificationDay_year_width}}} ' \
                    '{{beginCluster: <{beginCluster_width}}}\n'

        print_str = ''
        print_str += format_str.format(name='Filename', status='Status', createdTime_hour='createdTime_hour',
                                        createdTime_minute='createdTime_minute', createdTime_second='createdTime_second',
                                        createdTime_millisecond='createdTime_millisecond',
                                        createdDate_day='createdDate_day', createdDate_month='createdDate_month',
                                        createdDate_year='createdDate_year', latestAccessDay_day='latestAccessDay_day',
                                        latestAccessDay_month='latestAccessDay_month', latestAccessDay_year='latestAccessDay_year',
                                        latestModificationDay_day='latestModificationDay_day',
                                        latestModificationDay_month='latestModificationDay_month',
                                        latestModificationDay_year='latestModificationDay_year',
                                        beginCluster='Begin Cluster',
                                        name_width=max_width.get('name', 0), status_width=max_width.get('status', 0),
                                        createdTime_hour_width=max_width.get('createdTime_hour', 0),
                                        createdTime_minute_width=max_width.get('createdTime_minute', 0),
                                        createdTime_second_width=max_width.get('createdTime_second', 0),
                                        createdTime_millisecond_width=max_width.get('createdTime_millisecond', 0),
                                        createdDate_day_width=max_width.get('createdDate_day', 0),
                                        createdDate_month_width=max_width.get('createdDate_month', 0),
                                        createdDate_year_width=max_width.get('createdDate_year', 0),
                                        latestAccessDay_day_width=max_width.get('latestAccessDay_day', 0),
                                        latestAccessDay_month_width=max_width.get('latestAccessDay_month', 0),
                                        latestAccessDay_year_width=max_width.get('latestAccessDay_year', 0),
                                        latestModificationDay_day_width=max_width.get('latestModificationDay_day', 0),
                                        latestModificationDay_month_width=max_width.get('latestModificationDay_month', 0),
                                        latestModificationDay_year_width=max_width.get('latestModificationDay_year', 0),
                                        beginCluster_width=max_width.get('beginCluster', 0))

        for entry in entry_info_list:
            print(entry)

        return ""


    def list_entries(self):
        """
        Handler function for 'ls'
        """
        self.current_dir.build_tree()

        table = self.generate_table_view()
        print(table)

class FATDirectory(AbstractDirectory):
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

    def __init__(self, main_entry_buffer: bytes, parent_path: str, volume: FAT32, isrdet=False, lfn_entries=[]):
        # Dãy byte entry chính
        self.entry_buffer = main_entry_buffer
        self.volume = volume # con trỏ đến volume đang chứa thư mục này
        # Danh sách các subentry
        self.subentries = None

        # Nếu thư mục này là RDET (file thì ko cần xét RDET)
        if not isrdet:
            # Tên entry 
            if len(lfn_entries) > 0:
                lfn_entries.reverse()
                self.name = FAT32.process_fat_lfnentries(lfn_entries)
                lfn_entries.clear()
            else:
                self.name = read_bytes_buffer(main_entry_buffer, 0, 11).decode('utf-8', errors='ignore').strip()
            # Status
            self.attr = read_number_buffer(main_entry_buffer, 0xB, 1)

            # Các byte thấp và cao của chỉ số cluster đầu
            highbytes = read_number_buffer(main_entry_buffer, 0x14, 2)
            lowbytes = read_number_buffer(main_entry_buffer, 0x1A, 2)
            self.begin_cluster = highbytes * 0x100 + lowbytes
            self.path = parent_path + '/' + self.name
        else:
            self.name = read_bytes_buffer(main_entry_buffer, 0, 11).decode('utf-8', errors='ignore').strip()
            self.begin_cluster = self.volume.rdetStartCluster
            self.path = ''

        cluster_chain = self.volume.readRDETCluster(self.begin_cluster)
        self.sectors = self.volume.clusterToSector(cluster_chain)
        # Kích thước tập tin
        self.size = read_number_buffer(main_entry_buffer,0x1C,4)

        # Extracting created day and time
        created_date = read_number_buffer(main_entry_buffer, 0x10, 2)
        created_time = read_number_buffer(main_entry_buffer, 0x0D, 3)
        # create_milisec = read_bytes_buffer(main_entry_buffer, 0x0D, 1) 
        self.created_day, self.created_time = self.decode_datetime(created_date, created_time)

        # self.create_milisecond = int.from_bytes(create_milisec, byteorder='little')
        # Extracting latest modified day
        modified_date = read_number_buffer(main_entry_buffer, 0x18, 2)
        self.modified_day = self.decode_date(modified_date)

        access_day = read_number_buffer(main_entry_buffer, 0x12, 2)
        self.latest_access_day = self.decode_date(access_day)

    def decode_datetime(self, date_bytes, time_bytes):
        year = ((date_bytes >> 9) & 0x7F) + 1980
        month = (date_bytes >> 5) & 0x0C
        day = date_bytes & 0x1F

        # hour = (time_bytes >> 11) & 0x1F
        # minute = (time_bytes >> 5) & 0x3F
        # second = ((time_bytes & 0x1F) * 2)
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
            
    def build_tree(self):
        """
        Dựng cây thư mục cho thư mục này (đọc các sector trong mảng `self.sectors` được SDET rồi xử lý)
        """
        if self.subentries != None: 
            # Nếu đã dựng rồi thì ko làm lại nữa
            return 
        self.subentries = []
        subentry_index = 0

        # Đọc SDET (dữ liệu nhị phân) của thư mục
        sdet_buffer = read_sector_chain(self.volume.file_object, self.sectors, self.volume.nBytesPerSector)
        lfn_entries_queue = []

        while True:
            subentry_buffer = read_bytes_buffer(sdet_buffer, subentry_index, 32)
            # Read type
            entry_type = read_number_buffer(subentry_buffer, 0xB, 1)
            if entry_type & 0x10 == 0x10:
                # Là thư mục
                self.subentries.append(FATDirectory(subentry_buffer, self.path, self.volume, lfn_entries=lfn_entries_queue))
            elif entry_type & 0x20 == 0x20:
                # Là tập tin (archive)
                self.subentries.append(FATFile(subentry_buffer, self.path, self.volume, lfn_entries=lfn_entries_queue))
            elif entry_type & 0x0F == 0x0F:
                lfn_entries_queue.append(subentry_buffer)
            if entry_type == 0:
                break
            subentry_index += 32

    def print_tree(self, indent=0):
        """
        Recursively print out the directory tree with proper indentation
        """
        print("  " * indent + self.name + "/")
        if self.subentries:
            for entry in self.subentries:
                if isinstance(entry, FATDirectory):
                    entry.print_tree(indent + 1)
                else:
                    print("  " * (indent + 1) + entry.name)

    def build_and_print_tree(self):
        """
        Build and print the directory tree
        """
        self.build_tree()
        self.print_tree()

    def describe_attr(self):
        """
        Lấy chuỗi mô tả các thuộc tính
        """
        desc_map = {
            0x10: 'D',
            0x20: 'A',
            0x01: 'R', 
            0x02: 'H',
            0x04: 'S',
        }

        desc_str = ''
        for attribute in desc_map:
            if self.attr & attribute == attribute:
                desc_str += desc_map[attribute]
        
        return desc_str

class FATFile(AbstractFile):
    volume = None 
    name = None 
    attr = None 
    sectors = None
    path = None
    size = None
    created_day = None
    created_time = None
    modified_day = None

    def __init__(self, main_entry_buffer: bytes, parent_path: str, volume: FAT32, lfn_entries=[]):
        ...
        self.entry_buffer = main_entry_buffer
        self.volume = volume

        # Thuộc tính trạng thái
        self.attr = read_number_buffer(main_entry_buffer, 0xB, 1)

        # Tên entry 
        if len(lfn_entries) > 0:
            lfn_entries.reverse()
            self.name = FAT32.process_fat_lfnentries(lfn_entries)
            lfn_entries.clear()
        else:
            name_base = read_bytes_buffer(main_entry_buffer, 0, 8).decode('utf-8', errors='ignore').strip()
            name_ext = read_bytes_buffer(main_entry_buffer, 8, 3).decode('utf-8', errors='ignore').strip()
            self.name = name_base + '.' + name_ext

        
        # Phần Word(2 byte) cao
        highbytes = read_number_buffer(main_entry_buffer, 0x14, 2)
        # Phần Word (2 byte) thấp
        lowbytes = read_number_buffer(main_entry_buffer, 0x1A, 2)

        # Cluster bắt đầu
        self.begin_cluster = highbytes * 0x100 + lowbytes

        # Đường dẫn tập tin
        self.path = parent_path + '/' + self.name

        cluster_chain = self.volume.readRDETCluster(self.begin_cluster)
        self.sectors = self.volume.clusterToSector(cluster_chain)

        # Kích thước tập tin
        self.size = read_number_buffer(main_entry_buffer,0x1C,4)

        # Extracting created day and time
        created_date = read_number_buffer(main_entry_buffer, 0x10, 2)
        created_time = read_number_buffer(main_entry_buffer, 0x0D, 3)
        # create_milisec = read_bytes_buffer(main_entry_buffer, 0x0D, 1) 
        self.created_day, self.created_time = self.decode_datetime(created_date, created_time)

        # self.create_milisecond = int.from_bytes(create_milisec, byteorder='little')
        # Extracting latest modified day
        modified_date = read_number_buffer(main_entry_buffer, 0x18, 2)
        self.modified_day = self.decode_date(modified_date)

        access_day = read_number_buffer(main_entry_buffer, 0x12, 2)
        self.latest_access_day = self.decode_date(access_day)

    def decode_datetime(self, date_bytes, time_bytes):
        year = ((date_bytes >> 9) & 0x7F) + 1980
        month = (date_bytes >> 5) & 0x0C
        day = date_bytes & 0x1F

        # hour = (time_bytes >> 11) & 0x1F
        # minute = (time_bytes >> 5) & 0x3F
        # second = ((time_bytes & 0x1F) * 2)
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
        binary_data = read_sector_chain(self.volume.file_object, self.sectors, self.volume.bps)
        # "trim" bớt cho về đúng kích thước
        return binary_data[:self.size]

    def describe_attr(self):
        desc_map = {
            0x10: 'D',
            0x20: 'A',
            0x01: 'R', 
            0x02: 'H',
            0x04: 'S',
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
    fat32_volume.initialize_root_directory(f)
    fat32_volume.root_directory.build_and_print_tree()
    fat32_volume.list_entries()