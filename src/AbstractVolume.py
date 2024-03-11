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
            'nBytesPerSector'       : self.nBytesPerSector,
            'nSectorsPerCluster'    : self.nSectorsPerCluster,
            'nSectorsOnBootSector'  : self.nSectorsOnBootSector,
            'nSectorPerTrack'       : self.nSectorPerTrack,
            'nHead'                 : self.nHead,
            'sizeVolume'            : self.sizeVolume,
            'partitionType'         : self.partitionType,
        }
    
class AbstractEntry(metaclass=ABCMeta):
    """
    Lớp đối tượng thể hiện một entry
    """
    @property
    @abstractmethod
    def path(self) -> str:
        """
        Đường dẫn đến entry
        """
        pass

    @property
    @abstractmethod
    def volume(self) -> AbstractVolume:
        """
        Con trỏ đến volume chứa entry này (để truy cập vào bảng FAT/MFT và duyệt các cluster)
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Tên của thư mục này
        """
        pass

    @property
    @abstractmethod
    def attr(self) -> int:
        """
        Tên của thư mục này
        """
        pass

    @abstractmethod
    def describe_attr(self) -> str:
        """
        Diễn giải các thuộc tính dưới dạng chuỗi
        """
        pass

    @property
    @abstractmethod
    def sectors(self) -> int:
        """
        Là mảng các chỉ số sector chứa dữ liệu nhị phân của SDET/RDET của thư mục này
        """
        pass

class AbstractDirectory(AbstractEntry):
    @property
    @abstractmethod
    def subentries(self) -> list:
        """
        Mảng của các subentries (file/subdirectory) của thư mục này.
        """
        pass

class AbstractFile(AbstractEntry):
    @property
    @abstractmethod
    def size(self) -> int:
        """
        Kích thước (byte) của file
        """
        pass

    @abstractmethod
    def dump_binary_data(self) -> bytes:
        pass