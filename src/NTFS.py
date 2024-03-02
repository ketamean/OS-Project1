from AbstractVolume import AbstractVolume
from LowLevel import readSector

class NTFS(AbstractVolume):
    """
    OEMID                       = b''   # [byte] OEM ID in NTFS partition boot sector
    nBytesPerFileRecordSegment  = 0     # [int] number of clusters per file record segment
    nClustersPerIndexBuffer     = 0     # [int] number of clusters per index buffer
    volumeSerialNum             = ''    # [str] serial number của volume
    startingClusterMFT          = 0     # [int] logical cluster number (index) of file MFT ($Mft)
    startingClusterMFT          = 0     # [int] logical cluster number (index) file MFT Mirror ($MftMirr)
    """
    PARTITION_TYPE              = 'NTFS'
    def __init__(self, fileobj, beginsectorVBR = 0) -> None:
        self.__readVBR(fileobj=fileobj, beginsectorVBR=beginsectorVBR)
    def __readVBR(self, fileobj, beginsectorVBR = 0) -> None:
        """
            read NTFS partition boot sector to collect info and initialize the current NTFS volume (call `super().__init__()`)
        """
        firstsector = readSector(fileobject=fileobj, nsector=1, beginSector=beginsectorVBR)
        if firstsector[36:40] != b'\x80\x00\x80\x00':
            print(firstsector[36:40])
            raise TypeError('This is not an NTFS volume')
        nBytesPerSector                     = int.from_bytes(bytes=firstsector[11:13], byteorder='little')
        nSectorsPerCluster                  = int.from_bytes(firstsector[13:14], byteorder='little')
        nSectorsOnBootSector                = 16    # the first sector is the boot sector
                                                    # the next 15 sector is the boot sector's IPL (initial program loader) 
        nSectorPerTrack                     = int.from_bytes(firstsector[24:26], byteorder='little')
        nHead                               = int.from_bytes(firstsector[26:28], byteorder='little')
        sizeVolume                          = int.from_bytes(firstsector[40:48], byteorder='little')
        super().__init__(nBytesPerSector, nSectorsPerCluster, nSectorsOnBootSector, nSectorPerTrack, nHead, sizeVolume, NTFS.PARTITION_TYPE)

        self.startingClusterMFT             = int.from_bytes(firstsector[48:56], byteorder='little')
        self.OEMID                          = firstsector[3:11]
        self.nBytesPerFileRecordSegment     = 2**abs((int.from_bytes(bytes=firstsector[64:65], byteorder='little', signed=True)))
        self.nClustersPerIndexBuffer        = int.from_bytes(bytes=firstsector[68:69], byteorder='little', signed=True)
        self.volumeSerialNum                = firstsector[72:80].hex().upper()
    
    def getInfo(self) -> dict:
        res = super().getInfo()
        res['startingClusterMFT']           = self.startingClusterMFT
        res['OEMID']                        = self.OEMID
        res['nBytesPerFileRecordSegment']  = self.nBytesPerFileRecordSegment
        res['nClustersPerIndexBuffer']       = self.nClustersPerIndexBuffer
        res['volumeSerialNum']              = self.volumeSerialNum
        return res
    def buildDirectoryTree(self):
        raise NotImplementedError
    
if __name__ == '__main__':
    # this is for testing
    print('Testing...')
    with open('test/drive_ntfs.bin', 'rb') as f:
        tmp = NTFS(f)
        print("Info:", tmp.getInfo())
    print('Tested')