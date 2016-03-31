from partHelp import *
from sys import exit

import ext4.superblock as superblock
import ext4.groupDescriptor as groupDescriptor


class ext4:

   #this is the lazy way of doing this, it will have to be upgraded to a generator later
    def buildGroupDescriptors(self):
        """
        Builds the group descriptors for the class. 
        Note: only uses the first Block. Needs to be expanded to check other blocks to make sure these are corrupted

        Args: 
        None
        Return:
        None
        Creates:
        self.groupDescs (A list of ext2.groupDescriptor)
        """
        self.groupDescs = []
        #need to pull out the location first for speed purposes
        descGroupHex = getLocation(0x40 * (self.superblock.desc_block_num), 0x1200)
        for groupDescInd in range(self.superblock.desc_block_num):
            self.groupDescs.append(groupDescriptor.groupDescriptor(getHex(descGroupHex, 0x40*groupDescInd, 0x40+0x40*groupDescInd), self.superblock))


    def __init__(self, part):
        self.part_start = part['start']*512
        self.superblock = superblock.superblock(getLocation(0x400, self.part_start + 0x400))
        self.buildGroupDescriptors()
        print(self.superblock.groups_in_flex)
        print(self.superblock.block_size)

        print(self.groupDescs[7].bg_free_blocks_count_lo)
        #TODO: Figure out where the first group descriptors are


