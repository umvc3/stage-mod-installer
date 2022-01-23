import os
import struct
import zlib


class Arc(object):
    def __init__(self, arc_file_path):
        self.cmp_levels = {0x7801: 0,
                           0x789C: 6,
                           0x78DA: 9}
        self.arc_file_path = arc_file_path

        with open(arc_file_path, 'rb') as f:
            data = f.read()

        self.file_count = struct.unpack('<H', data[6:8])[0]

        self.path_list = []
        self.file_cmp = []
        self.binaries = []

        start = 0x8
        entry_length = 0x50

        for i in range(self.file_count):
            file_entry = struct.unpack('<64sLLLL',
                                       data[start + (entry_length * i):start + (entry_length * i) + entry_length])

            full_path = file_entry[0]
            full_path = full_path.split(b'\0', 1)[0]
            path_only = os.path.split(full_path)[0]

            data_length = file_entry[2]
            uncompressed_length = file_entry[3] - 0x40000000
            data_start = file_entry[4]

            data_end = data_start + data_length

            try:
                dec = zlib.decompress(data[data_start:data_end], zlib.MAX_WBITS, uncompressed_length)

                full_path += b'.' + b"%08x" % file_entry[1]
                full_path += b'.' + struct.unpack('3s', dec[0:3])[0].lower()

                self.path_list.append(full_path)
                self.file_cmp.append(struct.unpack('>H', data[data_start:data_start + 2])[0])

                #print(full_path.decode('utf-8'))
                self.binaries.append(dec)
            except zlib.error as e:
                pass


    def save(self, outfile):
        file_list = self.path_list

        file_entries = struct.pack('<3sxBxH0x', b'ARC', 0x07, len(file_list))
        deflated_data = b''
        file_entries_length = 0x8 + 0x50 * len(file_list)

        # Round up to nearest 32 bytes
        if file_entries_length % 32 != 0:
            file_entries_length = ((file_entries_length // 32) + 1) * 32

        for i in range(len(file_list)):
            filename = file_list[i]

            cmp_lvl = self.cmp_levels.get(self.file_cmp[i], 6)

            split_path = os.path.splitext(filename)[0]
            split_path = os.path.splitext(split_path)

            name_only = split_path[0]
            ext = int(split_path[1][1:], 16)

            file_entries += struct.pack('<64sI', name_only, ext)

            file_str = self.binaries[i]

            data_position = (file_entries_length + len(deflated_data))

            comp = zlib.compress(file_str, cmp_lvl)

            deflated_data += comp
            real_len = len(file_str) | 0x40000000
            file_entries += struct.pack('<III', len(comp), real_len, data_position)
            #print('Packing ' + filename)

        for i in range(len(file_entries), file_entries_length):
            file_entries += struct.pack('<B', 0)

        file_entries += deflated_data

        with open(outfile, 'wb') as f:
            f.write(file_entries)

    # def replace(self, file_to_replace, file_in):
    #     for i in range(len(self.path_list)):
    #         if self.path_list[i] == file_to_replace:
    #             with open(file_in, 'rb') as f:
    #                 self.binaries[i] = f.read()
    def replace(self, file_to_replace, data):
        for i in range(len(self.path_list)):
            if self.path_list[i] == file_to_replace:
                self.binaries[i] = data
