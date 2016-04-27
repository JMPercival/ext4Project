import partData
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
        descGroupHex = getLocation(0x40 * (self.superblock.desc_block_num), self.part_start+self.superblock.block_size, self.filesystem_to_use) if self.superblock.s_feature_incompat_dict['INCOMPAT_64BIT'] == True else getLocation(0x20 * (self.superblock.desc_block_num), self.part_start+self.superblock.block_size, self.filesystem_to_use)
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
        num = num - 1 #there is not 0 inode so we shift what we asked for down to comply with FS
        inode_block_group = int(num/self.superblock.s_inodes_per_group)
        inode_block_group_location = self.inode_tables_location_to_groups[inode_block_group]
        inode_inside_block_group = int(num%self.superblock.s_inodes_per_group)
        inode_inside_block_group_location = inode_inside_block_group * self.superblock.s_inode_size
        inode_final_location = int(inode_block_group_location + inode_inside_block_group_location)

        newInode = inode.inode(getLocation(self.superblock.s_inode_size, inode_final_location, self.filesystem_to_use), self.superblock)
        return newInode

    def getDirectoryBlocks(self, inode):
        inode_extent = extent.extent(getHex(inode.part, 0x28, 0x64, False), self.superblock, self.part_start)
        dir_list = ''
        for extent_record in inode_extent.ext4_extent_list_ordered:
            #TODO: work on initialized and uninitialized extent block
            dir_list += getLocation(extent_record[1] * self.superblock.block_size, self.part_start + extent_record[2] * self.superblock.block_size, self.filesystem_to_use)
        return dir_list

    def getDirectoryList(self, inode):
        directory_block = self.getDirectoryBlocks(inode)
        directoryList = []


        if inode.i_flags_dict['EXT4_INDEX_FL'] == False:
            new_directory_block = directory_block
        else:
            #TODO: figure out how interior nodes are placed on FS
            #TODO: add actual hashing like they do in the kernel rather than this linear search
            new_directory_block = getHex(directory_block, 0, 0x18) + getHex(directory_block, 0x28+(8*int(getHex(directory_block,0x22, 0x24),16)), len(directory_block))

        count=0
        while directory_block != '':
            count+=1
            newDir = directory.directory(directory_block,self.superblock)
            if newDir.inode != 0:
                directoryList.append(newDir)
            directory_block = directory_block[newDir.rec_len*2:]

        return directoryList


    def __init__(self, part, filesystem_to_use):
        self.filesystem_to_use = filesystem_to_use
        self.part_start = part['start']*512
        self.superblock = superblock.superblock(getLocation(0x400, self.part_start + 0x400, self.filesystem_to_use), self.filesystem_to_use)
        self.buildGroupDescriptors()
        self.buildLocations()
        root_directory_inode = self.getInode(2)
        self.current_dir_list = self.getDirectoryList(root_directory_inode)

        print(self.inode_tables_location_to_groups)
        print(self.superblock.groups_in_flex)
        print(self.superblock.block_size)
        print(self.superblock.desc_block_num)

        print(self.getInode(1482).part)
        print(len(self.getInode(12).part))
        print(self.getInode(1482).i_flags_dict['EXT4_INDEX_FL'])
        thisInode = self.getInode(2)
        print(self.getDirectoryList(thisInode)[0].inode)


    #Here starts the things I can ask the filesystem after all this building
    def userLoadDir(self, inode_num):
        return self.userLS(self.getDirectoryList(self.getInode(int(inode_num))))

    def userCD(self, dir):
        if dir == '':
            self.buildRootDir()
            return 0 #operation successful return code

        for dir_object in self.current_dir_list:
            if dir == dir_object.decoded_name and dir_object.isFiletype() and partData.directory_type[dir_object.file_type] == 'Directory':
                self.userCDSwitchDir(dir_object)
                return 0 #operation successful return code
            elif dir_object.isFiletype() == False:
                return 1 #filetype operation not supported... your in trouble
            elif dir == dir_object.decoded_name and dir_object.isFiletype() and partData.directory_type[dir_object.file_type] != 'Directory':
                return 2 #Can not cd into file return code
        return 3 #can not find file return code

    def userCDSwitchDir(self, dir_object):
        new_directory_inode = self.getInode(dir_object.inode)
        self.current_dir_list = self.getDirectoryList(new_directory_inode)

    def userLS(self, dir_object_list=''):
        dir_list_to_iter = []
        if dir_object_list == '':
            dir_list_to_iter = self.current_dir_list
        else:
            dir_list_to_iter = dir_object_list

        dir_list = []
        for dir_object in dir_list_to_iter:
            temp_dir_dict = {}
            temp_dir_dict['inode'] = dir_object.inode

            dir_object_inode = self.getInode(dir_object.inode)
            permission_bitmap = getBitmap(dir_object_inode.i_mode, 12)
            permission_string = 'x' if permission_bitmap[0] else '-'
            permission_string += 'w' if permission_bitmap[1] else '-'
            permission_string += 'r' if permission_bitmap[2] else '-'
            permission_string += 'x' if permission_bitmap[3] else '-'
            permission_string += 'w' if permission_bitmap[4] else '-'
            permission_string += 'r' if permission_bitmap[5] else '-'
            permission_string += 'x' if permission_bitmap[6] else '-'
            permission_string += 'w' if permission_bitmap[7] else '-'
            permission_string += 'r' if permission_bitmap[8] else '-'
            #permission_string += partData.directory_type_letter[dir_object.file_type]
            permission_string = permission_string[::-1]
            permission_string = list(permission_string)
            if permission_bitmap[9]:permission_string[0] = 'S'
            if permission_bitmap[10]:permission_string[4] = 'S'
            if permission_bitmap[11]:permission_string[1] = 'S'
            permission_string = ''.join(permission_string)

            temp_dir_dict['permission'] = permission_string
            #TODO: this will fail if the filesystem does not use INCOMPAT_FILETYPE... Probably best to fix this later
            temp_dir_dict['filetype'] = partData.directory_file_type[dir_object.file_type]

            temp_dir_dict['uid'] = dir_object_inode.i_uid
            temp_dir_dict['gid'] = dir_object_inode.i_gid
            temp_dir_dict['size'] = dir_object_inode.i_size
            i_atime = dir_object_inode.i_atime_date.split()
            temp_dir_dict['access_time'] = ' '.join(i_atime[1:4])
            #print('{0}\t{1}\t{2}\t{3}\t{4}\t'.format(permission_string, uid, gid, size, overall_time) ,end='')
            temp_dir_dict['name'] = dir_object.decoded_name

            dir_list.append(temp_dir_dict)

        return dir_list

    def userCAT(self, inode_num):
        inode_num = int(inode_num)
        data_encoded = self.getDirectoryBlocks(self.getInode(inode_num))
        data_decoded = ''.join([chr(int(data_encoded[c:c+2], 16)) for c in range(0, len(data_encoded), 2)])
        return data_decoded

    def getSuperblockVars(self):
        varString = ''
        for key in self.superblock.__dict__.keys():
            varString += key + ": " + self.superblock.__dict__[key] + '\n'
        return varString

    def getGroupDescVars(self):
        varString = ''
        count = 0
        for groupDesc in self.groupDescs:
            varString += 'Group Descriptor #'+count+':\n'
            count += 1
            for key in self.groupDesc.__dict__.keys():
                varString += key + ": " + self.groupDesc.__dict__[key] + '\n'
            varString += '\n\n'
        return varString