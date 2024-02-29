import AbstractPartition

class FAT32(AbstractPartition):
    """ ngoài các properties kế thừa từ parent class, class FAT32 còn có thêm các properties
    
    nFatTable               = 0         # [int] số bảng FAT
    sizeFatTable            = 0         # [int] kích thước mỗi bảng FAT
    rdetStartCluster        = 0         # [int] chỉ số cluster bắt đầu của RDET
    """
    # def __new__(cls):
    #     return super().__new__()
    def __init__(self, diskname) -> None:
        super().__init__(nBytesPerSector, nSectorsPerCluster, nSectorsOnBootSector, nSectorPerTrack, nHead, sizeVolume, partitionType)
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