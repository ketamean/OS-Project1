
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

def readBuffer(buffer, offset, size=1) -> bytes:
    """
    Hàm đọc chuỗi từ buffer tại vị trí `offset` với kích thước `size`.
    Nếu offset ở hệ 16 thì viết thêm tiền tố `0x`. Vd: `0x0DC`.
    HÀM CHƯA XỬ LÝ LITTLE ENDIEN
    
    Ví dụ: đọc tên file trên entry chính (8 byte tại offset `00`).
    >>> read_string(buffer, '00', 8)
    >>> read_string(buffer, 0, 8)
    """
        
    return buffer[offset:offset+size]

def readSectorBuffer(file_object, sector_list, bps=512):
    """
    Hàm đọc một dãy các sector từ mảng.
    Trả về: buffer đọc được.
    """
    buffer = b''
    for sector in sector_list:
        buffer += readSector(file_object, 1, sector, bps)
    return buffer
