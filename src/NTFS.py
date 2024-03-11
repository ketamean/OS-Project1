from AbstractVolume import AbstractVolume
from LowLevel import readSector, HexToBin
from OSItem import OSFile, OSFolder

def filetime_to_datetime(filetime):
    """
        convert a filetime number (which is the number of 100nanoseconds from Jan 1st 1601 up to date)
    """
    from datetime import datetime, timedelta
    EPOCH_AS_FILETIME   = 116444736000000000                    # January 1, 1970 as file time (number of 100nanoseconds)
    microsec            = (filetime - EPOCH_AS_FILETIME) // 10  # number of microsecond that the given filetime differs from 1/1/1970
    return datetime(1970,1,1) + timedelta(microseconds=microsec)

class MFTEntry:
    """
        this class holds an MFT entry, or an MFT file record
    """
    
    ATTRIBUTE_CODE = {
        0x10    : '$STANDARD_INFORMATION',  # [int] code type of attribute $STANDARD_INFO
        0x20    : '$ATTRIBUTE_LIST',        # [int] code type of attribute $ATTRIBUTE_LIST
        0x30    : '$FILE_NAME',             # [int] code type of attribute $FILE_NAME
                                            # this attribute is always resident; ntfs convert long file names to short file name using a particular algorithm
        0x40    : '$OBJECT_ID',             # [int] code type of attribute $OBJECT_ID
                                            # ignore
        0x50    : '$SECURITY_DESCRIPTOR',   # [int] code type of attribute $SECURITY_DESCRIPTOR
        0x60    : '$VOLUME_NAME',           # [int] code type of attribute $VOLUME_NAME
                                            # ignore
        0x70    : '$VOLUME_INFORMATION',    # [int] code type of attribute $VOLUME_INFORMATION
                                            # ignore
        0x80    : '$DATA',                  # [int] code type of attribute $DATA
        0x90    : '$INDEX_ROOT',            # [int] code type of attribute $INDEX_ROOT
                                            # this attribute is always resident
        0xA0    : '$INDEX_ALLOCATION',      # [int] code type of attribute $INDEX_ALLOCATION
        0xB0    : '$BITMAP',                # [int] code type of attribute $BITMAP
        0xC0    : '$SYMBOLIC_LINK',         # [int] code type of attribute $SYMBOLIC_LINK
                                            # ignore
        0xD0    : '$REPARSE_POINT',         # [int] code type of attribute $REPARSE_POINT
                                            # ignore
        0xE0    : '$EA_INFORMATION',        # [int] code type of attribute $EA_INFORMATION
                                            # ignore
        0xF0    : '$EA',                    # [int] code type of attribute $EA_INFORMATION
                                            # ignore
        0x100   : '$LOGGED_UTILITY_STREAM', # [int] code type of attribute $LOGGED_UTILITY_STREAM
                                            # ignore
    }

    FILE_NAME_FLAG = {                  # store the flag name with its corresponding position 1-bit (0-based) in the flag
        # fyi: https://flatcap.github.io/linux-ntfs/ntfs/attributes/file_name.html
        0   : 'R',  # Read-only
        1   : 'H',  # Hidden
        2   : 'S',  # System
        5   : 'A',  # Archvie

        # these following flags will be ignored
        6   : 'D',      # Device
        7   : 'N',      # Normal
        8   : 'T',      # Temporary
        9   : 'SF',     # Sparse File
        10  : 'RP',     #
        11  : 'C',      #
        12  : 'O',      #
        13  : 'NCI',    #
        14  : 'E',      #
    }

    @staticmethod
    def __convert_attrcode_to_type(code):
        name = MFTEntry.ATTRIBUTE_CODE.get(code)
        if name == None:
            raise ValueError(f'Attribute Code: The value {code} does not correspond to any attribute.')
        return name

    @staticmethod
    def entryStatus_to_ositemStatus(status):
        res = ''
        for i in status:
            res += str(i)
        return res
    
    @staticmethod
    def __convert_flag_to_status(flag):
        """
            convert a given flag in the $FILE_NAME attribute to a list of properties such as Read-only, Hidden, System, Archive,...
            the argument `flag` must be a string in hex
            each status will be represented by its first letter
        """
        
        res = []
        flag = HexToBin(flag)
        n = 0
        for i in flag:
            if i == '1':
                n += 1
        for i in MFTEntry.FILE_NAME_FLAG.keys():
            if i > 5:
                break
            if flag[len(flag) - 1 - i] == '1':
                # the ith bit from the right (0-based: the rightmost bit is the 0th bit)
                res.append(MFTEntry.FILE_NAME_FLAG[i])
        return res
        
    @staticmethod
    def header_entry_flags(bytes):
        """
            return flag in_use, is_dir
        """
        n = int.from_bytes(bytes=bytes, byteorder='little')
        return n & 0x01, (n & 0x02) >> 1
    

    def __init__(self, buffer, byte_per_record, fileobj, byte_per_cluster, byte_per_sector) -> None:
        """
            input a buffer byte stream for a particular entry.

            essential information will be extracted

            all the properties that an MFT entry has will be all declared here
        """
        # some important info
        self.__buffer               = buffer
        self.__disk_obejct          = fileobj
        self.__byte_per_cluster     = byte_per_cluster
        self.__byte_per_sector      = byte_per_sector
        self.__byte_per_record      = byte_per_record

        # in $STANDARD_INFORMATION
        self.signature              = ''
        self.offset_first_attr      = None
        self.in_use                = None
        self.is_dir                 = None
        self.used_size              = None
        self.alloc_size             = None
        self.base_record_file_ref   = None      # stream of bytes
        self.createdTime            = None
        self.createdDate            = None
        self.latestModificationDay  = None
        self.latestAccessDay        = None

        # in entry header
        self.id                     = None

        # in $FILE_NAME
        self.parent_id              = None
        self.status                 = None      # S(ystem), A(rchive), H(idden),......
        self.name                   = None

        # in $VOLUME_NAME
        self.volume_name            = None

        # in $DATA
        self.readable               = None      
        self.data                   = None      # content of the file if this is a readable (text file)
            # these following properties will be None in resident $DATA
        self.data_alloc_size        = None      # rounded up to a cluster size (disk alloc by cluster to reduce indexing processes)
        self.data_real_size         = None      # 
        self.data_init_size         = None

        self.__parse_entry()

    def __parse_volume_name(self, attr_buffer):
        # double check
        if int.from_bytes(bytes=attr_buffer[0x00:0x04], byteorder='little') != 0x60:
            return
        # resident
        content_size    = int.from_bytes(bytes=attr_buffer[16:20], byteorder='little')
        begin_content   = int.from_bytes(bytes=attr_buffer[20:22], byteorder='little')
        self.volume_name = attr_buffer[begin_content:begin_content + content_size].decode('utf-16-le')

    def __parse_standard_information(self, attr_buffer):
        # double check
        if int.from_bytes(bytes=attr_buffer[0x00:0x04], byteorder='little') != 0x10:
            return
        # resident
        content_size    = int.from_bytes(bytes=attr_buffer[16:20], byteorder='little')
        begin_content   = int.from_bytes(bytes=attr_buffer[20:22], byteorder='little')

        # created time
        crTime = filetime_to_datetime(
            int.from_bytes(bytes=attr_buffer[begin_content:begin_content + 8], byteorder='little')
        )
        self.createdTime = {}
        self.createdTime['millisecond']     = crTime.microsecond // 1000
        self.createdTime['second']          = crTime.second
        self.createdTime['minute']          = crTime.minute
        self.createdTime['hour']            = crTime.hour
        
        # created date
        self.createdDate = {}
        self.createdDate['day']             = crTime.day
        self.createdDate['month']           = crTime.month
        self.createdDate['year']            = crTime.year

        # latest modification date
        latestmodify = filetime_to_datetime(
            int.from_bytes(bytes=attr_buffer[begin_content + 8:begin_content + 16], byteorder='little')
        )
        self.latestModificationDay = {}
        self.latestModificationDay['day']   = latestmodify.day
        self.latestModificationDay['month'] = latestmodify.month
        self.latestModificationDay['year']  = latestmodify.year
        
        # latest access date
        latestaccess = filetime_to_datetime(
            int.from_bytes(bytes=attr_buffer[begin_content + 24:begin_content + 32], byteorder='little')
        )
        self.latestAccessDay = {}
        self.latestAccessDay['day']         = latestaccess.day
        self.latestAccessDay['month']       = latestaccess.month
        self.latestAccessDay['year']        = latestaccess.year

    def __parse_entry_header(self):
        """
            extract info from buffer of the header of an entry
            returns false it this is not an entry; otherwise, returns nothing
        """
        buffer                  = self.__buffer
        self.signature          = buffer[0:4].decode('ascii')
        if self.signature != 'FILE':
            return False

        # relative offset of the first attribute in the current record
        self.offset_first_attr  = int.from_bytes(bytes=buffer[0x14:0x14 + 2], byteorder='little')
        # flags on the header of the MFT file record
        self.in_use,self.is_dir= MFTEntry.header_entry_flags(buffer[22:24])
        # number of bytes the current record occupies
        self.used_size          = int.from_bytes(bytes=buffer[24:28], byteorder='little')
        self.alloc_size         = int.from_bytes(bytes=buffer[28:32], byteorder='little')

        self.base_record_file_ref = buffer[32:40]

        self.id                 = int.from_bytes(bytes=buffer[44:48], byteorder='little')

    def __parse_data(self, attr_buffer):
        """
            parse data attribute of a file record
        """
        # double check
        if int.from_bytes(bytes=attr_buffer[0x00:0x04], byteorder='little') != 0x80:
            return
        attr_resident    = not bool(attr_buffer[8])
        if not attr_resident:
            self.data_alloc_size    = int.from_bytes(bytes=attr_buffer[0x28:0x28 + 8], byteorder='little')
            self.data_real_size     = int.from_bytes(bytes=attr_buffer[0x30:0x30 + 8], byteorder='little')
            self.data_init_size     = int.from_bytes(bytes=attr_buffer[0x38:0x38 + 8], byteorder='little')
        ############################################################
        def isTextFile(filename: str):
            if filename and filename.endswith('.txt'):
                return True
            return False
        
        if not isTextFile(self.name):
            self.readable   = False
            self.data       = None
            return
        self.readable       = True
        self.data           = ''
        
        if attr_resident:
            begin_content   = int.from_bytes(bytes=attr_buffer[20:22], byteorder='little')
            content_size    = int.from_bytes(bytes=attr_buffer[16:20], byteorder='little')
            self.data       = attr_buffer[begin_content:begin_content + content_size].decode('utf-8')
        else:
            lcn             = 0     # logical cluster number of the volume
            datarun_offset  = int.from_bytes(bytes=attr_buffer[0x20:0x22], byteorder='little')
            cluster_list    = []    # (lcn, ncluster from that point)
            def readRun(offset_byte):
                # returns ncluster, lcn, new_offset_datarun
                header      = int.from_bytes(bytes=attr_buffer[offset_byte:offset_byte + 1], byteorder='little')
                size_len    = (header & 0x0F)
                size_offset = (header & 0xF0) >> 4
                length      = int.from_bytes(bytes=attr_buffer[offset_byte + 1:offset_byte + 1 + size_len], byteorder='little')
                if size_offset == 0:
                    vcn     = 0
                else:
                    vcn     = int.from_bytes(bytes=attr_buffer[offset_byte + 1 + size_len:offset_byte + 1 + size_len + size_offset], byteorder='little', signed=True)
                return length, vcn, offset_byte + size_offset + size_len + 1

            while datarun_offset < len(attr_buffer) and attr_buffer[datarun_offset] != 0:
                ncluster, vcn, datarun_offset = readRun(datarun_offset)
                # vcn can be negative
                if vcn != 0:
                    lcn += vcn
                    cluster_list.append( (ncluster, lcn) )
            for ncluster, lcn in cluster_list:
                raw_data    = readSector(
                    fileobject=self.__disk_obejct,
                    nsector=ncluster * self.__byte_per_cluster // self.__byte_per_sector,
                    beginSector=lcn * self.__byte_per_cluster // self.__byte_per_sector,
                    bytePerSector=self.__byte_per_sector
                )
                self.data   += raw_data.decode('utf-8')

    def __parse_filename(self, attr_buffer):
        """
            short name only => always resident
        """
        # double check
        if int.from_bytes(bytes=attr_buffer[0x00:0x04], byteorder='little') != 0x30:
            return
        # resident
        content_size    = int.from_bytes(bytes=attr_buffer[16:20], byteorder='little')
        begin_content   = int.from_bytes(bytes=attr_buffer[20:22], byteorder='little')
        self.parent_id  = int.from_bytes(bytes=attr_buffer[begin_content:begin_content + 6], byteorder='little')
        self.status     = MFTEntry.__convert_flag_to_status(flag=attr_buffer[56:60].hex())
        len_name        = int.from_bytes(bytes=attr_buffer[begin_content + 64:begin_content + 65], byteorder='little')
        # # test
        # print('filename.name_buffer:',attr_buffer[begin_content + 66:begin_content + 66 + 2*len_name])
        self.name       = attr_buffer[begin_content + 66:begin_content + 66 + 2*len_name].decode('utf-16-le')

    def __parse_attribute(self, buffer):
        # printBuffer(buffer)
        attr_type           = MFTEntry.__convert_attrcode_to_type(
            code=int.from_bytes(bytes=buffer[0:4], byteorder='little')
        )
        
        attr_nonresident    = int(buffer[8:9].hex(), 16)
        attr_name_len       = int(buffer[9:10].hex(), 16)                                 # name of the attribute
        offset_to_name      = int.from_bytes(bytes=buffer[10:12], byteorder='little')
        
        if attr_type == '$STANDARD_INFORMATION':
            # resident
            self.__parse_standard_information(attr_buffer=buffer)
        elif attr_type == '$VOLUME_NAME':
            # resident
            self.__parse_volume_name(attr_buffer=buffer)
        elif attr_type == '$FILE_NAME':
            # resident
            self.__parse_filename(attr_buffer=buffer)
        elif attr_type == '$DATA':
            # resident or non-resident
            self.__parse_data(attr_buffer=buffer)
        elif attr_type == '$INDEX_ROOT' or attr_type == '$INDEX_ALLOCATION' or attr_type == '$BITMAP':
            self.is_dir = True

    def __parse_entry(self):
        succ                    = self.__parse_entry_header()
        self.is_dir             = False # initially False
        if succ == False:
            return
        buffer                  = self.__buffer
        
        attr_offset             = self.offset_first_attr    # current position, or a pointer points to the current attribute in the record
        # read atributes in the file record
        while attr_offset < self.__byte_per_record and buffer[attr_offset] != 255:
            attr_len            = int.from_bytes(bytes=buffer[attr_offset + 4:attr_offset + 8], byteorder='little')
            # # test
            # print('attr type:', MFTEntry.__convert_attrcode_to_type(int.from_bytes(bytes=buffer[attr_offset:attr_offset + 4],byteorder='little')))
            self.__parse_attribute(buffer=buffer[attr_offset:attr_offset + attr_len])
            attr_offset         += attr_len

class NTFS(AbstractVolume):
    """
    OEMID                       = b''   # [byte] OEM ID in NTFS partition boot sector
    nBytesPerFileRecord         = 0     # [int] number of clusters per file record segment
    nClustersPerIndexBuffer     = 0     # [int] number of clusters per index buffer
    volumeSerialNum             = ''    # [str] serial number của volume
    startingClusterMFT          = 0     # [int] logical cluster number (index) of file MFT ($Mft)
    startingClusterMFTMirr      = 0     # [int] logical cluster number (index) file MFT Mirror ($MftMirr)

    root                        =       # [OSFolder] the root directory as an OSFolder

    __disk_object               = f     # the file object points to the volume that we are working on
    """
    PARTITION_TYPE              = 'NTFS'
    def __readVBR(self, beginsectorVBR = 0) -> None:
        """
            read NTFS partition boot sector to collect info and initialize the current NTFS volume (call `super().__init__()`)
        """
        firstsector = readSector(fileobject=self.__disk_object, nsector=1, beginSector=beginsectorVBR)
        # if firstsector[36:40] != b'\x80\x00\x80\x00':
        #     print(firstsector[36:40])
        #     raise TypeError('This is not an NTFS volume')
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
        self.nBytesPerFileRecord            = 2**abs((int.from_bytes(bytes=firstsector[64:65], byteorder='little', signed=True)))
        self.nClustersPerIndexBuffer        = int.from_bytes(bytes=firstsector[68:69], byteorder='little', signed=True)
        self.volumeSerialNum                = firstsector[72:80].hex().upper()
    
    def __init__(self, fileobj, beginsector_vbr = 0):
        # some important information
        self.__disk_object  = fileobj
        self.volume_name    = ''

        self.__id_to_entry    = {}    # [dict] map an entry's id with the object entry
        self.__entry_to_id    = {}    # [dict] map an entry with its id
        self.__root         = None  # [OSFolder] the root directory as an OSFolder
                                    # these the above 2 properties are used for building directory tree
        
        self.__readVBR( beginsectorVBR=beginsector_vbr )
        self.__build()

    def __clusterToSector(self, ncluster) -> int:
        return self.nSectorsPerCluster * ncluster
    
    def __build_ositem_relation(self):
        """
            read all entries/file record in MFT and build relations of OSItem in the directory tree 
        """
        def get_file_extension(name: str):
            return name[name.rfind('.') + 1:]
        n_entry             = 1
        cnt                 = 0
        self.__id_to_ositem = {}    # [dict] map an ositem's id with an ositem object (osfile or osfolder)
        self.__ositem_to_id = {}    # [dict] map an ositem with its id
        self.__id_to_entry  = {}    # [dict] map an entry's id with an entry object
        self.__entry_to_id  = {}    # [dict] map an entry with its id

        while n_entry > 0:
            buffer = readSector(
                fileobject=self.__disk_object,
                nsector=self.nBytesPerFileRecord // self.nBytesPerSector,
                beginSector=self.startingClusterMFT * self.nSectorsPerCluster + cnt * self.nBytesPerFileRecord // self.nBytesPerSector,
                bytePerSector=self.nBytesPerSector
            )

            entry = MFTEntry(
                buffer=buffer,
                byte_per_cluster=self.nBytesPerSector * self.nSectorsPerCluster,
                fileobj=self.__disk_object,
                byte_per_record=self.nBytesPerFileRecord,
                byte_per_sector=self.nBytesPerSector
            )
            # đọc trong MFT (MFT coi như một mảng), record nào hợp lệ ((id > 24 or id == 5) and parent hợp lệ) thì mới được đưa vào
            # Khi đọc thì sẽ gặp parent trước. Nếu parent không hợp lệ => không được đưa vào list => không xuất hiện trong list <=> get() == None
            # => cái entry hiện tại đang xét cũng không cần quan tâm luôn
            if (
                entry.in_use and
                entry.id and (entry.id > 24 or entry.id == 5) and
                entry.parent_id and (entry.parent_id > 24 or entry.parent_id == 5) and
                ( ################################ mới thêm điều kiện này
                    self.__id_to_entry.get(entry.parent_id) or
                    entry.parent_id == 5
                )
            ):
                self.__id_to_entry[entry.id]    = entry
                self.__entry_to_id[entry]       = entry.id
                if entry.is_dir:
                    ositem = OSFolder(
                        name=entry.name,
                        status=MFTEntry.entryStatus_to_ositemStatus(entry.status),
                        createdDate_day=entry.createdDate['day'],
                        createdDate_month=entry.createdDate['month'],
                        createdDate_year=entry.createdDate['year'],
                        createdTime_hour=entry.createdTime['hour'],
                        createdTime_minute=entry.createdTime['minute'],
                        createdTime_second=entry.createdTime['second'],
                        createdTime_millisecond=entry.createdTime['millisecond'],
                        latestAccessDay_day=entry.latestAccessDay['day'],
                        latestAccessDay_month=entry.latestAccessDay['month'],
                        latestAccessDay_year=entry.latestAccessDay['year'],
                        latestModificationDay_day=entry.latestModificationDay['day'],
                        latestModificationDay_month=entry.latestModificationDay['month'],
                        latestModificationDay_year=entry.latestModificationDay['year'],
                        idxStartingCluster=self.startingClusterMFT + entry.id * ((self.nBytesPerFileRecord // self.nBytesPerSector) // self.nSectorsPerCluster),
                        size=entry.alloc_size
                    )
                else:
                    ositem = OSFile(
                        name=entry.name if entry.name.rfind('.') < 0 else entry.name[:entry.name.rfind('.')],
                        extension=get_file_extension(entry.name),
                        status=MFTEntry.entryStatus_to_ositemStatus(entry.status),
                        createdDate_day=entry.createdDate['day'],
                        createdDate_month=entry.createdDate['month'],
                        createdDate_year=entry.createdDate['year'],
                        createdTime_hour=entry.createdTime['hour'],
                        createdTime_minute=entry.createdTime['minute'],
                        createdTime_second=entry.createdTime['second'],
                        createdTime_millisecond=entry.createdTime['millisecond'],
                        latestAccessDay_day=entry.latestAccessDay['day'],
                        latestAccessDay_month=entry.latestAccessDay['month'],
                        latestAccessDay_year=entry.latestAccessDay['year'],
                        latestModificationDay_day=entry.latestModificationDay['day'],
                        latestModificationDay_month=entry.latestModificationDay['month'],
                        latestModificationDay_year=entry.latestModificationDay['year'],
                        idxStartingCluster=self.startingClusterMFT + entry.id * ((self.nBytesPerFileRecord // self.nBytesPerSector) // self.nSectorsPerCluster),
                        size=entry.alloc_size,
                        data=entry.data
                    )
                self.__id_to_ositem[entry.id]   = ositem
                self.__ositem_to_id[ositem]     = entry.id     

            if entry.volume_name:
                self.volume_name    = entry.volume_name
            if entry.name == '$MFT':
                n_entry             = entry.data_real_size // self.nBytesPerFileRecord
            
            n_entry -= 1
            cnt     += 1

            # print(entry.name)
            # print('\t >', entry.status)


    def __build_directory_tree(self):
        """
            build the directory tree of the current volume instance
        """
        # root folder is the 5th entry (0-based) in the NTFS MFT
        self.__id_to_ositem[5].name = self.volume_name

        for id, ositem in self.__id_to_ositem.items():
            if id == 5:
                continue
            parent_ositem = self.__id_to_ositem[ self.__id_to_entry[id].parent_id ]  
            # print(ositem.name, 'in', parent_ositem.name)
            parent_ositem.children.append(ositem)
        
        self.__root = self.__id_to_ositem[5]

    def __build(self):
        self.__build_ositem_relation()
        self.__build_directory_tree()

    def getInfo(self):
        res = super().getInfo()
        res['startingClusterMFT']       = self.startingClusterMFT
        res['OEMID']                    = self.OEMID
        res['nBytesPerFileRecord']      = self.nBytesPerFileRecord
        res['nClustersPerIndexBuffer']  = self.nClustersPerIndexBuffer
        res['volumeSerialNum']          = self.volumeSerialNum
        return res

    def getDirectoryTree(self):
        """
            get root folder of the current volume's directory tree
        """
        return self.__root

if __name__ == '__main__':
    with open('\\\\.\\D:', 'rb') as f:
        tmp = NTFS(f)
        root = tmp.getDirectoryTree()

        # test
        root.access(0)