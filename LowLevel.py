
"""
    file gồm các function để giao tiếp với low level system
"""

def HexToDec(hex: str) -> int:
    """
        chuyển từ [str] hexadecimal sang [int] decimal
    """
    return int(hex, 16)

def readSector(diskpath, nsector, beginSector = 0, bytePerSector = 512):
    """
        đọc `nsector` trong partition của `diskpath`, bắt đầu từ sector `beginSector` (0-based). Mặc định mỗi sector lá 512 bytes
    """
    with open(diskpath, 'rb') as f:
        f.seek(beginSector * bytePerSector)
        f.read(nsector * bytePerSector)


def readBytes(diskpath: str, offset = 0, nBytes = 1):
    """
        đọc `nBytes` byte (mặc định là đọc 1byte) từ ổ đĩa `diskpath`, bắt đầu offset `offset`
    """
    with open(diskpath, 'rb') as f:
        pass

def accessDirectoryTree():
    pass

