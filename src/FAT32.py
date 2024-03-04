from AbstractVolume import AbstractVolume
from LowLevel import readSector

class FAT32(AbstractVolume):
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
        self.dataStartSector = 0        # [int] sector bắt đầu của vùng dữ liệu

        # Đọc thông tin từ boot sector để set properties    
        buffer = readSector(fileobject, 1)

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

        # Đọc bảng FAT
        FATbuffer = readSector(fileobject, self.sizeFatTable, self.nSectorsOnBootSector + 1)
        print(FATbuffer)

        # Đọc bảng RDET
        # clusterChain = self.readRDETCluster(self.rdetStartCluster, FATbuffer)
        # sectorChain = self.clusterToSector(clusterChain)
        # RDETbuffer = readSector(fileobject, sectorChain.__sizeof__,  sectorChain)

    def readRDETCluster(self, startCluster, FATbuffer) -> list:
        """
        Hàm dùng để dò bảng FAT ra dãy cluster của RDET, bắt đầu từ startCluster
        """
        # Kiểm tra cluster kết thúc
        eoCluster = [0, 268435440, 268435455, 268435447, 268435448, 4294967280]
        if startCluster in eoCluster:
            return []
        
        nextCluster = startCluster
        chain = [nextCluster]

        while True:
            # Bảng FAT bỏ 2 phần tử đầu, bắt đầu từ 0 -> phần tử 2 = cluster 1
            nextCluster = int.from_bytes(FATbuffer[nextCluster * 4:nextCluster * 4 + 4], 'little')
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
            # Tìm begin sector của vùng dữ liệu, tương ứng cluster trên vùng dữ liệu đánh số từ 2
            beginSector = self.dataStartSector * (cluster - 2) * self.nSectorsPerCluster
            for sector in range(beginSector, beginSector + self.nSectorsPerCluster):
                chain.append(sector)
        return chain
    
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