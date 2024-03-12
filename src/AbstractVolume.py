from abc import ABCMeta, abstractmethod

class AbstractVolume:
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
    sizeVolume              = 0         # [int] số sector của volume
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
            'Number of bytes per sector'                : self.nBytesPerSector,
            'Number of sectors per cluster'             : self.nSectorsPerCluster,
            'Number of sectors on boot sector region'   : self.nSectorsOnBootSector,
            'Number of sectors per track'               : self.nSectorPerTrack,
            'Number of head on disk'                    : self.nHead,
            'Total size of the volume'                  : self.sizeVolume,
            'Partition type'                            : self.partitionType,
        }
    