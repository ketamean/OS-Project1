class AbstractPartition:
    """
        đây là abstract class đại diện cho các loại partition: FAT32, NTFS

        class này giữ các thông tin chung cho của partition
    """
    """
    nBytesPerSector         = 0         # [int] số byte trong mỗi sector, thường là 512
    nSectorsPerCluster      = 0         # [int] số sector trong mỗi cluster
    nSectorsOnBootSector    = 0         # [int] số sector trên vùng boot sector
    nSectorPerTrack         = 0         # [int] số sector trên mỗi track
    nHead                   = 0         # [int] số lượng đầu đọc trên đĩa
    sizeVolume              = 0         # [int] kích thước volume
    partitionType           = ''        # [str] kiểu partion
                                        # = 'FAT32' hoặc = 'NTFS'
    """
    def __init__(
            self, nBytesPerSector: int, nSectorsPerCluster: int, nSectorsOnBootSector: int, nSectorPerTrack: int,
            nHead: int, sizeVolume: int, partitionType: str
    ) -> None:
        if not (
            isinstance(nBytesPerSector, int)        and
            isinstance(nSectorsPerCluster, int)     and
            isinstance(nSectorsOnBootSector, int)   and
            isinstance(nSectorPerTrack, int)        and
            isinstance(nHead, int)                  and
            isinstance(sizeVolume, int)             and
            isinstance(partitionType, str)
        ):
            raise TypeError("Cannot init partition: Wrong data type of parameters")
        
        if not (partitionType == 'FAT32' or partitionType == 'NTFS'):
            raise ValueError('Cannot init partition: incorrect type of partition (partition must be \'FAT32\' or \'NTFS\')')
        self.nBytesPerSector        = nBytesPerSector
        self.nSectorsPerCluster     = nSectorsPerCluster
        self.nSectorsOnBootSector   = nSectorsOnBootSector
        self.nSectorPerTrack        = nSectorPerTrack
        self.nHead                  = nHead
        self.sizeVolume             = sizeVolume
        self.partitionType          = partitionType
    
    def getInfo(self):
        return {
            'nBytesPerSector'       : self.nBytesPerSector,
            'nSectorsPerCluster'    : self.nSectorsPerCluster,
            'nSectorsOnBootSector'  : self.nSectorsOnBootSector,
            'nSectorPerTrack'       : self.nSectorPerTrack,
            'nHead'                 : self.nHead,
            'sizeVolume'            : self.sizeVolume,
            'partitionType'         : self.partitionType,
        }

class FAT32(AbstractPartition):
    """ ngoài các properties kế thừa từ parent class, class FAT32 còn có thêm các properties
    
    nFatTable               = 0         # [int] số bảng FAT
    sizeFatTable            = 0         # [int] kích thước mỗi bảng FAT
    rdetStartCluster        = 0         # [int] chỉ số cluster bắt đầu của RDET
    """
    # def __new__(cls):
    #     return super().__new__()
    def __init__(self, nBytesPerSector: int, nSectorsPerCluster: int, nSectorsOnBootSector: int, nFatTable: int, nSectorPerTrack: int, nHead: int, sizeVolume: int, sizeFatTable: int, rdetStartCluster: int, partitionType: str) -> None:
        super().__init__(nBytesPerSector, nSectorsPerCluster, nSectorsOnBootSector, nSectorPerTrack, nHead, sizeVolume, sizeFatTable, rdetStartCluster, partitionType)    
    def getInfo(self):
        res = super().getInfo()
        res['sizeFatTable']         = self.sizeFatTable
        res['rdetStartCluster']     = self.rdetStartCluster
        res['nFatTable']            = self.nFatTable
        return res
    def buildDirectoryTree(self):
        raise NotImplementedError

class NTFS(AbstractPartition):
    # def __new__(cls):
    #     return super().__new__()
    def __init__(self, nBytesPerSector: int, nSectorsPerCluster: int, nSectorsOnBootSector: int, nFatTable: int, nSectorPerTrack: int, nHead: int, sizeVolume: int, sizeFatTable: int, rdetStartCluster: int, partitionType: str) -> None:
        super().__init__(nBytesPerSector, nSectorsPerCluster, nSectorsOnBootSector, nFatTable, nSectorPerTrack, nHead, sizeVolume, sizeFatTable, rdetStartCluster, partitionType)    
    
    def buildDirectoryTree(self):
        raise NotImplementedError
    

if __name__ == '__main__':
    # test initializers
    print('Testing...')
    tmp = FAT32(1,2,3,4,5,6,7,8,9, 'FAT32')
    tmp = NTFS(1,2,3,4,5,6,7,8,9, 'NTFS')
    print("Info:", tmp.getInfo())
    print('Tested')