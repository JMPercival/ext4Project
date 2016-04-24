from partHelp import *

class extent:
    class ext4_extent_idx:
        def __init__(self, part, superblock):
            self.part = part
            self.ei_block= int(getHex(self.part, 0x0, 0x4, True),16)# /* This index node covers file blocks from 'block' onward. */
            self.ei_leaf_lo= int(getHex(self.part, 0x4, 0x8, True),16)# /* Lower 32-bits of the block number of the extent node that is the next level lower in the tree. The tree node pointed to can be either another internal node or a leaf node, described below. */
            self.ei_leaf_hi= int(getHex(self.part, 0x8, 0xa, True),16)# /* Upper 16-bits of the previous field. */
            self.ei_unused= int(getHex(self.part, 0xa, 0xc, True),16)

            self.ei_leaf =  self.ei_leaf_lo + (self.ei_leaf_hi<<32)

    class ext4_extent:
        def __init__(self, part, superblock):
            self.part = part
            self.ee_block= int(getHex(self.part, 0x0, 0x4, True),16)# /* First file block number that this extent covers. */
            self.ee_len= int(getHex(self.part, 0x4, 0x6, True),16)# /* Number of blocks covered by extent. If the value of this field is <= 32768, the extent is initialized. If the value of the field is > 32768, the extent is uninitialized and the actual extent length is ee_len - 32768. Therefore, the maximum length of a initialized extent is 32768 blocks, and the maximum length of an uninitialized extent is 32767. */
            self.ee_start_hi= int(getHex(self.part, 0x6, 0x8, True),16)# /* Upper 16-bits of the block number to which this extent points. */
            self.ee_start_lo= int(getHex(self.part, 0x8, 0xc, True),16)# /* Lower 32-bits of the block number to which this extent points. */

            self.ee_start = self.ee_start_lo + (self.ee_start_hi<<32)

    class ext4_extent_tail: #this is currently being ignored... probably a good idea to implement at a later date
        def __init__(self, part, superblock):
            self.part = part
            self.eb_checksum= int(getHex(self.part, 0x0, 0x4, True),16)# /* Checksum of the extent block, crc32c(uuid+inum+igeneration+extentblock) */

    def __init__(self, part, superblock, part_start):
        self.part = part
        self.eh_magic= int(getHex(self.part, 0x0, 0x2, True),16)# /* Magic number, 0xF30A. */
        self.eh_entries= int(getHex(self.part, 0x2, 0x4, True),16)# /* Number of valid entries following the header. */
        self.eh_max= int(getHex(self.part, 0x4, 0x6, True),16)# /* Maximum number of entries that could follow the header. */
        self.eh_depth= int(getHex(self.part, 0x6, 0x8, True),16)# /* Depth of this extent node in the extent tree. 0 = this extent node points to data blocks; otherwise, this extent node points to other extent nodes. The extent tree can be at most 5 levels deep: a logical block number can be at most 2^32, and the smallest n that satisfies 4*(((blocksize - 12)/12)^n) >= 2^32 is 5. */
        self.eh_generation= int(getHex(self.part, 0x8, 0xc, True),16)# /*Generation of the tree. (Used by Lustre, but not standard ext4). */


        self.ext4_extent_list = []
        #self.ext4_extent_class = []
        for entry_num in range(self.eh_entries):
            if self.eh_depth == 0:
                self.ext4_extent_list.append(self.ext4_extent(getHex(self.part, entry_num*12 + 0xc, entry_num*12 + 0xc +0xc, False)))
            else:
                cur_idx = self.ext4_extent_idx(getHex(self.part, entry_num*12 + 0xc, entry_num*12 + 0xc +0xc, False))
                #TODO: figure out what ext4_extent_idx.ei_block is/does
                cur_new_class = extent(getLocation(superblock.block_size, part_start +cur_idx.ei_leaf * superblock.block_size, superblock), superblock, part_start)
                self.ext4_extent_list += cur_new_class.ext4_extent_list
                #self.ext4_extent_class.append(cur_new_class)

        self.ext4_extent_list_ordered = []
        for extent_record in self.ext4_extent_list:
            self.ext4_extent_list_ordered.append([extent_record.ee_block, extent_record.ee_len, entry_num.ee_start])
        sorted(self.ext4_extent_list_ordered, key=lambda extent_record: extent_record[0])
