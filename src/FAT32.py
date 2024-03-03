from AbstractVolume import AbstractPartition
from LowLevel import readSector

class FAT32(AbstractPartition):
    """ ngoài các properties kế thừa từ parent class, class FAT32 còn có thêm các properties
    
    nFatTable               = 0         # [int] số bảng FAT
    sizeFatTable            = 0         # [int] kích thước mỗi bảng FAT
    rdetStartCluster        = 0         # [int] chỉ số cluster bắt đầu của RDET
    """
    # def __new__(cls):
    #     return super().__new__()
    def __init__(self, fileobject) -> None:
        # Khởi tạo các properties của class
        self.nFatTable = 0              # [int] số bảng FAT
        self.sizeFatTable = 0           # [int] kích thước mỗi bảng FAT
        self.rdetStartCluster = 0       # [int] chỉ số cluster bắt đầu của RDET

        # Đọc thông tin từ boot sector để set properties
        self.readBootSector(fileobject)
        super().__init__(self.nBytesPerSector, self.nSectorsPerCluster, self.nSectorsOnBootSector, self.nSectorPerTrack, self.nHead, self.sizeVolume, self.partitionType)

    def readBootSector(self, fileobject):
        # Đọc các thông tin chung của partition

    
        buffer = readSector(fileobject, 1)
        # print(buffer)

        self.nBytesPerSector = int.from_bytes(buffer[11:13], byteorder='little')
        self.nSectorsPerCluster = int.from_bytes(buffer[13:14], byteorder='little')
        self.nSectorsOnBootSector = int.from_bytes(buffer[14:16], byteorder='little')
        self.nSectorPerTrack = int.from_bytes(buffer[24:26], byteorder='little')
        self.nHead = int.from_bytes(buffer[26:28], byteorder='little')
        self.sizeVolume = int.from_bytes(buffer[32:36], byteorder='little')

        # Đọc các thông tin của FAT32
        self.nFatTable = int.from_bytes(buffer[16:17], byteorder='little')
        self.sizeFatTable = int.from_bytes(buffer[36:40], byteorder='little')
        self.rdetStartCluster = int.from_bytes(buffer[44:48], byteorder='little')
        self.partitionType = buffer[82:90].decode('utf-8').strip()

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
    with open('test/drive_fat.bin', 'rb') as f:
        tmp = FAT32(f)
        print(tmp)
        print("Info:", tmp.getInfo())
    print('Tested')