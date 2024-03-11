
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

def read_bytes_buffer(buffer, offset, size=1) -> bytes:
    """
    Hàm đọc chuỗi từ buffer tại vị trí `offset` với kích thước `size`.
    Nếu offset ở hệ 16 thì viết thêm tiền tố `0x`. Vd: `0x0DC`.
    
    Ví dụ: đọc tên file trên entry chính (8 byte tại offset `00`).
    >>> read_string(buffer, '00', 8)
    >>> read_string(buffer, 0, 8)
    """
        
    return buffer[offset:offset+size]
    
def read_entry_buffer(buffer, offset, size) -> int:
    """
    Hàm đọc số nguyên không dấu từ buffer tại vị trí `offset` với kích thước `size`.
    Nếu offset viết theo hex, truyền vào dưới dạng chuỗi (vd: '0B', '0D', ...)
    Nếu offset viết ở hệ 10, truyền vào dưới dạng số (vd: 110, 4096, ...)
    Hàm này đã xử lý số little endian.
    
    Cách dùng tương tự `read_string_buffer`
    """
    buffer = read_bytes_buffer(buffer, offset, size)
    hex_buffer = buffer[::-1].hex()
    return HexToDec(hex_buffer)

def read_number_buffer(buffer: bytes, start_index: int, length: int) -> int:
    hex_str = buffer[start_index:start_index + length].hex()
    if hex_str:
        return HexToDec(hex_str)
    else:
        return 0

def read_sector_chain(file_object, sector_list, bps=512):
    """
    Hàm đọc một dãy các sector từ mảng.
    Trả về: buffer đọc được.
    """
    buffer = b''
    for sector in sector_list:
        buffer += readSector(file_object, 1, sector, bps)
    return buffer
