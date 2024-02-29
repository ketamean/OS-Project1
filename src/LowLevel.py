
"""
    file gồm các function để giao tiếp với low level system
"""

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
    fileobject.seek(beginSector * bytePerSector)
    return fileobject.read(nsector * bytePerSector)