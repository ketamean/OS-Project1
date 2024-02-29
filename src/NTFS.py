import AbstractPartition

class NTFS(AbstractPartition):
    # def __new__(cls):
    #     return super().__new__()
    def __init__(self) -> None:
        super().__init__(nBytesPerSector, nSectorsPerCluster, nSectorsOnBootSector, nSectorPerTrack, nHead, sizeVolume, partitionType)
    
    def buildDirectoryTree(self):
        raise NotImplementedError
    
if __name__ == '__main__':
    # this is for testing
    print('Testing...')
    tmp = NTFS('test/drive_fat.bin')
    print("Info:", tmp.getInfo())
    print('Tested')