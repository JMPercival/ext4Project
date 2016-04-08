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

        Args: None
        Return: None
        Creates: self.groupDescs (A list of ext4.groupDescriptor)
        """
        self.groupDescs = []
        #need to pull out the location first for speed purposes
        #TODO: line will be buggy if superblock.block_size is <= 1024
        descGroupHex = getLocation(0x40 * (self.superblock.desc_block_num), self.part_start+self.superblock.block_size) if self.superblock.s_feature_incompat_dict['INCOMPAT_64BIT'] == True else getLocation(0x20 * (self.superblock.desc_block_num), self.part_start+self.superblock.block_size)
        for groupDescInd in range(self.superblock.desc_block_num):
            self.groupDescs.append(groupDescriptor.groupDescriptor(getHex(descGroupHex, 0x40*groupDescInd, 0x40+0x40*groupDescInd), self.superblock)) if self.superblock.s_feature_incompat_dict['INCOMPAT_64BIT'] == True else self.groupDescs.append(groupDescriptor.groupDescriptor(getHex(descGroupHex, 0x20*groupDescInd, 0x20+0x20*groupDescInd), self.superblock))


    def __init__(self, part):
        self.part_start = part['start']*512
        self.superblock = superblock.superblock(getLocation(0x400, self.part_start + 0x400))
        self.buildGroupDescriptors()
        print(self.superblock.groups_in_flex)
        print(self.superblock.block_size)
        print(self.superblock.desc_block_num)

        print(self.groupDescs[14].part)
        #TODO: Figure out where the first group descriptors are


