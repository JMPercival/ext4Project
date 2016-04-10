from partHelp import *

class groupDescriptor:
    def __init__(self, part, superblock):
        self.part = part

        self.bg_block_bitmap_lo= int(getHex(self.part, 0x0, 0x4, True), 16)#Lower 32-bits of location of block bitmap.
        self.bg_inode_bitmap_lo= int(getHex(self.part, 0x4, 0x8, True), 16)#Lower 32-bits of location of inode bitmap.
        self.bg_inode_table_lo= int(getHex(self.part, 0x8, 0xc, True), 16)#Lower 32-bits of location of inode table.
        self.bg_free_blocks_count_lo= int(getHex(self.part, 0xC, 0xe, True), 16)#Lower 16-bits of free block count.
        self.bg_free_inodes_count_lo= int(getHex(self.part, 0xE, 0x10, True), 16)#Lower 16-bits of free inode count.
        self.bg_used_dirs_count_lo= int(getHex(self.part, 0x10, 0x12, True), 16)#Lower 16-bits of directory count.
        self.bg_flags= int(getHex(self.part, 0x12, 0x14, True), 16)#None
        self.bg_exclude_bitmap_lo= int(getHex(self.part, 0x14, 0x18, True), 16)#Lower 32-bits of location of snapshot exclusion bitmap.
        self.bg_block_bitmap_csum_lo= int(getHex(self.part, 0x18, 0x1a, True), 16)#Lower 16-bits of the block bitmap checksum.
        self.bg_inode_bitmap_csum_lo= int(getHex(self.part, 0x1A, 0x1c, True), 16)#Lower 16-bits of the inode bitmap checksum.
        self.bg_itable_unused_lo= int(getHex(self.part, 0x1C, 0x1e, True), 16)#None

        #TODO: add the check to see if this should be added
        self.bg_checksum= int(getHex(self.part, 0x1E, 0x20, True), 16)#Group descriptor checksum; crc16(sb_uuid+group+desc) if the RO_COMPAT_GDT_CSUM feature is set, or crc32c(sb_uuid+group_desc) & 0xFFFF if the RO_COMPAT_METADATA_CSUM feature is set.


        #These only exist if the partition is 64bit
        if superblock.s_feature_incompat_dict['INCOMPAT_64BIT'] == True and superblock.s_desc_size > 32:
            #TODO: check if these should be here(64bit feature and s_desc_size>32)
            self.bg_block_bitmap_hi= int(getHex(self.part, 0x20, 0x24, True), 16)#Upper 32-bits of location of block bitmap.
            self.bg_inode_bitmap_hi= int(getHex(self.part, 0x24, 0x28, True), 16)#Upper 32-bits of location of inodes bitmap.
            self.bg_inode_table_hi= int(getHex(self.part, 0x28, 0x2c, True), 16)#Upper 32-bits of location of inodes table.
            self.bg_free_blocks_count_hi= int(getHex(self.part, 0x2C, 0x2e, True), 16)#Upper 16-bits of free block count.
            self.bg_free_inodes_count_hi= int(getHex(self.part, 0x2E, 0x30, True), 16)#Upper 16-bits of free inode count.
            self.bg_used_dirs_count_hi= int(getHex(self.part, 0x30, 0x32, True), 16)#Upper 16-bits of directory count.
            self.bg_itable_unused_hi= int(getHex(self.part, 0x32, 0x34, True), 16)#Upper 16-bits of unused inode count.
            self.bg_exclude_bitmap_hi= int(getHex(self.part, 0x34, 0x38, True), 16)#Upper 32-bits of location of snapshot exclusion bitmap.
            self.bg_block_bitmap_csum_hi= int(getHex(self.part, 0x38, 0x3a, True), 16)#Upper 16-bits of the block bitmap checksum.
            self.bg_inode_bitmap_csum_hi= int(getHex(self.part, 0x3A, 0x3c, True), 16)#Upper 16-bits of the inode bitmap checksum.
            self.bg_reserved= int(getHex(self.part, 0x3C, 0x40, False), 16)#Padding to 64 bytes.

            self.bg_block_bitmap = self.bg_block_bitmap_lo + (self.bg_block_bitmap_hi << 32)
            self.bg_inode_bitmap = self.bg_inode_bitmap_lo + (self.bg_inode_bitmap_hi <<32)
            self.bg_inode_table = self.bg_inode_table_lo + (self.bg_inode_table_hi<<32)
            self.bg_free_blocks_count = self.bg_free_blocks_count_lo + (self.bg_free_blocks_count_hi<<16)
            self.bg_free_inodes_count = self.bg_free_inodes_count_lo + (self.bg_free_inodes_count_hi<<16)
            self.bg_used_dirs_count = self.bg_used_dirs_count_lo + (self.bg_used_dirs_count_hi<<16)
            self.bg_exclude_bitmap = self.bg_exclude_bitmap_lo + (self.bg_exclude_bitmap_hi<<32)
            self.bg_block_bitmap_csum = self.bg_block_bitmap_csum_lo + (self.bg_block_bitmap_csum_hi<<16)
            self.bg_inode_bitmap_csum = self.bg_inode_bitmap_csum_lo + (self.bg_inode_bitmap_hi<<16)

        else:
            self.bg_block_bitmap = self.bg_block_bitmap_lo
            self.bg_inode_bitmap = self.bg_inode_bitmap_lo
            self.bg_inode_table = self.bg_inode_table_lo
            self.bg_free_blocks_count = self.bg_free_blocks_count_lo
            self.bg_free_inodes_count = self.bg_free_inodes_count_lo
            self.bg_used_dirs_count = self.bg_used_dirs_count_lo
            self.bg_exclude_bitmap = self.bg_exclude_bitmap_lo
            self.bg_block_bitmap_csum = self.bg_block_bitmap_csum_lo
            self.bg_inode_bitmap_csum = self.bg_inode_bitmap_csum_lo

