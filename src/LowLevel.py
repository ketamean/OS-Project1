
"""
    file gồm các function để giao tiếp với low level system
"""

def HexToBin(hex: str) -> str:
    """
        convert a string of hexadecimal to a corresponding string of binary
    """
    val = int(hex, 16)
    res = ''
    while val > 0: # avoid getting leading zeroes
        res = str(val % 2) + res
        val = val >> 1
    return res

def HexToDec(hex: str) -> int:
    """
        nhận [str] hexadecimal và trả về [int] decimal
    """
    return int(hex, 16)

def readSector(fileobject, nsector, beginSector = 0, bytePerSector = 512):
    """
        đọc `nsector` trong partition của `fileobject`, bắt đầu từ sector `beginSector` (0-based: sector đầu tiên là sector số 0). Mặc định mỗi sector lá 512 bytes

        lưu ý: trước khi gọi hàm thì người dùng tự mở file/ổ đĩa sau đó truyền hẳn file object vào
    """
    offset = beginSector * bytePerSector
    if fileobject.tell() != offset:
        fileobject.seek(offset)
    return fileobject.read(nsector * bytePerSector)