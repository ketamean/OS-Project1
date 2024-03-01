from AbstractVolume import AbstractPartition

class FAT32(AbstractPartition):
    """ ngoài các properties kế thừa từ parent class, class FAT32 còn có thêm các properties
    
    nFatTable               = 0         # [int] số bảng FAT
    sizeFatTable            = 0         # [int] kích thước mỗi bảng FAT
    rdetStartCluster        = 0         # [int] chỉ số cluster bắt đầu của RDET
    """
    # def __new__(cls):
    #     return super().__new__()
    def __init__(self, diskname) -> None:
        nBytesPerSector = 512
        nSectorsPerCluster = 8
        nSectorsOnBootSector = 1
        nSectorPerTrack = 1
        nHead = 1
        sizeVolume = 100
        partitionType = 'FAT32'
        
        super().__init__(nBytesPerSector, nSectorsPerCluster, nSectorsOnBootSector, nSectorPerTrack, nHead, sizeVolume, partitionType)
        # Khởi tạo các properties của class
        self.nfatTable = 0              # [int] số bảng FAT
        self.sizeFatTable = 0           # [int] kích thước mỗi bảng FAT
        self.rdetStartCluster = 0       # [int] chỉ số cluster bắt đầu của RDET

        # Đọc thông tin từ boot sector để set properties
        self.readBootSector(diskname)

    def readBootSector(self, diskname):
        # Mở ổ đĩa
        with open(diskname, 'rb') as f:
            # Tìm kiếm vị trí bắt đầu của boot sector + đọc
            f.seek(self.nSectorsOnBootSector * self.nBytesPerSector)
            bootSector = f.read(self.nBytesPerSector)

            # Trong trường hợp boot sector bao gồm 2 trường byte cho nFatTable
            # self.nfatTable = struct.unpack('<H', bootSector[0x10:0x12][0])

    def getInfo(self):
        res = super().getInfo()
        res['sizeFatTable']         = self.sizeFatTable
        res['rdetStartCluster']     = self.rdetStartCluster
        res['nFatTable']            = self.nFatTable
        return res
    
    def buildDirectoryTree(self):
        raise NotImplementedError
    
if __name__ == '__main__':
    # this is for testing
    print('Testing...')
    tmp = FAT32('test/drive_fat.bin')
    print("Info:", tmp.getInfo())
    print('Tested')