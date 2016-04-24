from partHelp import *
from sys import exit

import ext4.superblock as superblock
import ext4.groupDescriptor as groupDescriptor
import ext4.inode as inode
import ext4.extent as extent
import ext4.directory as directory

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
        #TODO: also, 0x40 needs to be replaced with superblock.s_desc_size instead of being hard coded
        descGroupHex = getLocation(0x40 * (self.superblock.desc_block_num), self.part_start+self.superblock.block_size) if self.superblock.s_feature_incompat_dict['INCOMPAT_64BIT'] == True else getLocation(0x20 * (self.superblock.desc_block_num), self.part_start+self.superblock.block_size)
        for groupDescInd in range(self.superblock.desc_block_num):
            self.groupDescs.append(groupDescriptor.groupDescriptor(getHex(descGroupHex, 0x40*groupDescInd, 0x40+0x40*groupDescInd), self.superblock)) if self.superblock.s_feature_incompat_dict['INCOMPAT_64BIT'] == True else self.groupDescs.append(groupDescriptor.groupDescriptor(getHex(descGroupHex, 0x20*groupDescInd, 0x20+0x20*groupDescInd), self.superblock))

    def buildLocations(self):
        """
        Builds the inode table, block bitmap, and inode bitmap locations

        Args:
            None
        Return:
            None
        Creates:
            self.inode_tables_location_to_groups (Dict of byte location for inodes)
            self.block_bitmaps (Dict of block and its block bitmap)
            self.inode_bitmaps (Dict of block and its inode bitmap)
        """
        self.inode_tables_location_to_groups = []
        self.block_bitmaps = []
        self.inode_bitmaps = []
        for groupDesc in self.groupDescs:
            self.inode_tables_location_to_groups.append(self.part_start + groupDesc.bg_inode_table * self.superblock.block_size)
            self.inode_bitmaps.append(self.part_start + groupDesc.bg_inode_table * self.superblock.block_size)
            self.block_bitmaps.append(self.part_start + groupDesc.bg_inode_table * self.superblock.block_size)

    def getInode(self, num):
<<<<<<< HEAD
        num = num - 1 #there is not 0 inode so we shift what we asked for down to comply with FS
        inode_block_group = int(num/self.superblock.s_inodes_per_group)
=======
        num = num - 1 #there is no 0 inode so we shift what we asked for down to comply with FS
        inode_block_group = int(num/int(self.sb.s_inodes_per_group,16))
>>>>>>> 410f621533dc0829d770bb7f99eaaaf9dc4d676d
        inode_block_group_location = self.inode_tables_location_to_groups[inode_block_group]
        inode_inside_block_group = int(num%self.superblock.s_inodes_per_group)
        inode_inside_block_group_location = inode_inside_block_group * self.superblock.s_inode_size
        inode_final_location = int(inode_block_group_location + inode_inside_block_group_location)

        newInode = inode.inode(getLocation(self.superblock.s_inode_size, inode_final_location), self.superblock)
        return newInode

    def getDirectoryBlocks(self, inode):
        inode_extent = extent(gethex(getHex(inode.part, 0x28, 0x64, False)))
        dir_list = ''
        for extent_record in inode_extent.ext4_extent_list_ordered:
            #TODO: work on initialized and uninitialized extent block
            dir_list += getLocation(part_start + extent_record.ee_start * superblock.block_size, extent_record.ee_len * superblock.block_size)
        return dir_list

    def buildDirectoryList(self, inode):
        directory_block = self.getDirectoryBlocks(inode)
        directoryList = []

        if inode.i_flags_dict['EXT4_INDEX_FL'] == False:
            count=0
            while raw_block != '':
                count+=1
                newDir = directory.directory(directory_block,self.superblock)
                directoryList.append(newDir)
                raw_block = raw_block[int(newDir.rec_len, 16)*2:]
        else:
            #TODO: hash tree stuff here
            pass

        return directoryList


    def __init__(self, part):
        self.part_start = part['start']*512
        self.superblock = superblock.superblock(getLocation(0x400, self.part_start + 0x400))
        self.buildGroupDescriptors()
        self.buildLocations()
        print(self.inode_tables_location_to_groups)
        print(self.superblock.groups_in_flex)
        print(self.superblock.block_size)
        print(self.superblock.desc_block_num)

        print(self.getInode(1482).part)
        print(len(self.getInode(12).part))
        print(self.getInode(1482).i_flags_dict['EXT4_INDEX_FL'])



'''
        for x in range(12, 2000):
            print(hex(self.getInode(x).i_mode))
            print(self.getInode(x).i_flags_dict['EXT4_INDEX_FL'])
            if self.getInode(x).i_flags_dict['EXT4_INDEX_FL'] == True:
                break
'''


        print(self.buildDirectoryList(2))


