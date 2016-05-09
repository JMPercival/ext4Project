from partHelp import *
import time


class inode:
    def i_flags_def(self):
        self.i_flags_dict={'EXT4_SECRM_FL':False,'EXT4_UNRM_FL':False,
                           'EXT4_COMPR_FL':False,'EXT4_SYNC_FL':False,
                           'EXT4_IMMUTABLE_FL':False,'EXT4_APPEND_FL':False,
                    #       'EXT4_NODUMP_FL':False,'EXT4_NOATIME_FL':False,
                           'EXT4_DIRTY_FL':False,'EXT4_COMPRBLK_FL':False,
                           'EXT4_NOCOMPR_FL':False,'EXT4_ENCRYPT_FL':False,
                         #  'EXT4_INDEX_FL':False,'EXT4_IMAGIC_FL':False,
                           'EXT4_JOURNAL_DATA_FL':False,'EXT4_NOTAIL_FL':False,
                           'EXT4_DIRSYNC_FL':False,'EXT4_TOPDIR_FL':False,
                       #    'EXT4_HUGE_FILE_FL':False,'EXT4_EXTENTS_FL':False,
                           'Not Used (0x100000)':False,'EXT4_EA_INODE_FL':False,
                           'EXT4_EOFBLOCKS_FL':False,'Not Used (0x800000)':False,
                           'EXT4_SNAPFILE_FL':False,'Not Used (0x2000000)':False,
                           'EXT4_SNAPFILE_DELETED_FL':False,'EXT4_SNAPFILE_SHRUNK_FL':False,
                           'EXT4_INLINE_DATA_FL':False,'EXT4_PROJINHERIT_FL':False,
                           'Not Used (0x40000000)':False,'EXT4_RESERVED_FL':False
                        }

        bitmap = getBitmap(self.i_flags, 32)
        #
        self.i_flags_dict['EXT4_SECRM_FL'] = bitmap[0]
        #
        self.i_flags_dict['EXT4_UNRM_FL'] = bitmap[1]
        #
        self.i_flags_dict['EXT4_COMPR_FL'] = bitmap[2]
        #
        self.i_flags_dict['EXT4_SYNC_FL'] = bitmap[3]
        #
        self.i_flags_dict['EXT4_IMMUTABLE_FL'] = bitmap[4]
        #
        self.i_flags_dict['EXT4_APPEND_FL'] = bitmap[5]
        #
        self.i_flags_dict['EXT4_NODUMP_FL'] = bitmap[6]
        #
        self.i_flags_dict['EXT4_NOATIME_FL'] = bitmap[7]
        #
        self.i_flags_dict['EXT4_DIRTY_FL'] = bitmap[8]
        #
        self.i_flags_dict['EXT4_COMPRBLK_FL'] = bitmap[9]
        #
        self.i_flags_dict['EXT4_NOCOMPR_FL'] = bitmap[10]
        #
        self.i_flags_dict['EXT4_ENCRYPT_FL'] = bitmap[11]
        #
        self.i_flags_dict['EXT4_INDEX_FL'] = bitmap[12]
        #
        self.i_flags_dict['EXT4_IMAGIC_FL'] = bitmap[13]
        #
        self.i_flags_dict['EXT4_JOURNAL_DATA_FL'] = bitmap[14]
        #
        self.i_flags_dict['EXT4_NOTAIL_FL'] = bitmap[15]
        #
        self.i_flags_dict['EXT4_DIRSYNC_FL'] = bitmap[16]
        #
        self.i_flags_dict['EXT4_TOPDIR_FL'] = bitmap[17]
        #
        self.i_flags_dict['EXT4_HUGE_FILE_FL'] = bitmap[18]
        #
        self.i_flags_dict['EXT4_EXTENTS_FL'] = bitmap[19]
        #
        self.i_flags_dict['Not Used (0x100000)'] = bitmap[20]
        #
        self.i_flags_dict['EXT4_EA_INODE_FL'] = bitmap[21]
        #
        self.i_flags_dict['EXT4_EOFBLOCKS_FL'] = bitmap[22]
        #
        self.i_flags_dict['Not Used (0x800000)'] = bitmap[23]
        #
        self.i_flags_dict['EXT4_SNAPFILE_FL'] = bitmap[24]
        #
        self.i_flags_dict['Not Used (0x2000000)'] = bitmap[25]
        #
        self.i_flags_dict['EXT4_SNAPFILE_DELETED_FL'] = bitmap[26]
        #
        self.i_flags_dict['EXT4_SNAPFILE_SHRUNK_FL'] = bitmap[27]
        #
        self.i_flags_dict['EXT4_INLINE_DATA_FL'] = bitmap[28]
        #
        self.i_flags_dict['EXT4_PROJINHERIT_FL'] = bitmap[29]
        #
        self.i_flags_dict['Not Used (0x40000000)'] = bitmap[30]
        #
        self.i_flags_dict['EXT4_RESERVED_FL'] = bitmap[31]


    def __init__(self, part, superblock):
        self.part = part
        self.i_mode= int(getHex(self.part, 0x0, 0x2, True),16)# /* File mode */
        self.i_uid= int(getHex(self.part, 0x2, 0x4, True),16)# /* Low 16 bits of Owner Uid */
        self.i_size_lo= int(getHex(self.part, 0x4, 0x8, True),16)#/* Size in bytes */
        self.i_atime= int(getHex(self.part, 0x8, 0xc, True),16)#* Access time */
        self.i_ctime= int(getHex(self.part, 0xc, 0x10, True),16)#/* Creation time */ This might actuall be Change time
        self.i_mtime= int(getHex(self.part, 0x10, 0x14, True),16)#* Modification time */
        self.i_dtime= int(getHex(self.part, 0x14, 0x18, True),16)#* * Deletion Time */
        self.i_gid= int(getHex(self.part, 0x18, 0x1a, True),16)#* Low 16 bits of Group Id */
        self.i_links_count= int(getHex(self.part, 0x1a, 0x1c, True),16)#/* Links count */
        self.i_blocks_lo= int(getHex(self.part, 0x1c, 0x20, True),16)#/* Blocks count */
        self.i_flags= int(getHex(self.part, 0x20, 0x24, True),16)#/* File flags */
        self.i_osd1= int(getHex(self.part, 0x24, 0x28, False),16)#/* OS dependent 1 */
        #TODO: emulate the union of structs for data in osd1
        #i_block big endian for now, I will flip the 32 bit values later
        self.i_block= int(getHex(self.part, 0x28, 0x64, False),16)#/* Pointers to blocks */
        self.i_generation= int(getHex(self.part, 0x64, 0x68, True),16)#/* File version (for NFS) */
        self.i_file_acl_lo= int(getHex(self.part, 0x68, 0x6c, True),16)#/* File ACL */
        self.i_size_high= int(getHex(self.part, 0x6c, 0x70, True),16)#/* Directory ACL */
        self.i_obso_faddr= int(getHex(self.part, 0x70, 0x74, True),16)#/* Fragment address */
        self.i_osd2= int(getHex(self.part, 0x74, 0x80, False),16)#/* OS dependent 2 */
        self.i_extra_isize= int(getHex(self.part, 0x80, 0x82, False),16)#/* Size of this inode - 128. Alternately, the size of the extended inode fields beyond the original ext2 inode, including this field. */
        self.i_checksum_hi= int(getHex(self.part, 0x82, 0x84, False),16)#/* Upper 16-bits of the inode checksum. */
        self.i_ctime_extra= int(getHex(self.part, 0x84, 0x88, False),16)#/* Extra change time bits. This provides sub-second precision. See Inode Timestamps section. */
        self.i_mtime_extra= int(getHex(self.part, 0x74, 0x8c, False),16)#/* Extra modification time bits. This provides sub-second precision. */
        self.i_atime_extra= int(getHex(self.part, 0x8c, 0x90, False),16)#/* Extra access time bits. This provides sub-second precision. */
        self.i_crtime= int(getHex(self.part, 0x90, 0x94, False),16)#/* File creation time, in seconds since the epoch. */
        self.i_crtime_extra= int(getHex(self.part, 0x94, 0x98, False),16)#/* Extra file creation time bits. This provides sub-second precision. */
        self.i_version_hi= int(getHex(self.part, 0x98, 0x9c, False),16)#/* Upper 32-bits for version number. */
        self.i_projid= int(getHex(self.part, 0x9c, 0xa0, False),16)#/* Project ID. */

        #TODO: emulate the union of structs for data in osd2

        self.i_flags_def()

        ##MY VARS
        self.i_atime_date=time.ctime(self.i_atime)
        self.i_ctime_date=time.ctime(self.i_ctime)
        self.i_mtime_date=time.ctime(self.i_mtime)
        self.i_dtime_date=time.ctime(self.i_dtime)
        self.i_crtime_date=time.ctime(self.i_crtime)

        #UNION OSD2 Linux
        #TODO: Add in the hurd and masix versions
        self.i_blocks_high=int(getHex(self.part, 0x74, 0x76, True),16)
        self.i_file_acl_high=int(getHex(self.part, 0x76, 0x78, True),16)
        self.i_uid_high=int(getHex(self.part, 0x78, 0x8a, True),16)
        self.i_gid_high=int(getHex(self.part, 0x8a, 0x8c, True),16)
        self.i_checksum_lo=int(getHex(self.part, 0x8c, 0x8e, True),16)
        self.i_reserved=int(getHex(self.part, 0x8e, 0x90, True),16)

        self.i_blocks_512 = not(superblock.s_feature_ro_compat_dict['RO_COMPAT_HUGE_FILE'] and self.i_flags_dict['EXT4_HUGE_FILE_FL'])
        self.i_blocks = self.i_blocks_lo + (self.i_blocks_high<<32) if superblock.s_feature_ro_compat_dict['RO_COMPAT_HUGE_FILE'] else self.i_blocks_lo
        self.i_file_acl =self.i_file_acl_lo + (self.i_file_acl_high<<32)
        self.i_uid = self.i_uid + (self.i_uid_high<<16)
        self.i_gid = self.i_gid + (self.i_gid_high<<16)
        self.i_checksum = self.i_checksum_lo + (self.i_checksum_hi<<16)
        self.i_size = self.i_size_lo + (self.i_size_high<<32)


        #Probably not used
        self.i_block_dict={
            'directBlock0' : int(getHex(self.part, 0x28, 0x2c, True),16) if int(getHex(self.part, 0x28, 0x2c, True),16) !=0 else False,
            'directBlock1' : int(getHex(self.part, 0x2c, 0x30, True),16) if int(getHex(self.part, 0x2c, 0x30, True),16) !=0 else False,
            'directBlock2' : int(getHex(self.part, 0x30, 0x34, True),16) if int(getHex(self.part, 0x30, 0x34, True),16) !=0 else False,
            'directBlock3' : int(getHex(self.part, 0x34, 0x38, True),16) if int(getHex(self.part, 0x34, 0x38, True),16) !=0 else False,
            'directBlock4' : int(getHex(self.part, 0x38, 0x3c, True),16) if int(getHex(self.part, 0x38, 0x3c, True),16) !=0 else False,
            'directBlock5' : int(getHex(self.part, 0x3c, 0x40, True),16) if int(getHex(self.part, 0x3c, 0x40, True),16) !=0 else False,
            'directBlock6' : int(getHex(self.part, 0x40, 0x44, True),16) if int(getHex(self.part, 0x40, 0x44, True),16) !=0 else False,
            'directBlock7' : int(getHex(self.part, 0x44, 0x48, True),16) if int(getHex(self.part, 0x44, 0x48, True),16) !=0 else False,
            'directBlock8' : int(getHex(self.part, 0x48, 0x4c, True),16) if int(getHex(self.part, 0x48, 0x4c, True),16) !=0 else False,
            'directBlock9' : int(getHex(self.part, 0x4c, 0x50, True),16) if int(getHex(self.part, 0x4c, 0x50, True),16) !=0 else False,
            'directBlock10' : int(getHex(self.part, 0x50, 0x54, True),16) if int(getHex(self.part, 0x50, 0x54, True),16) !=0 else False,
            'directBlock11' : int(getHex(self.part, 0x54, 0x58, True),16) if int(getHex(self.part, 0x54, 0x58, True),16) !=0 else False,
            'singleIndirect' : int(getHex(self.part, 0x58, 0x5c, True),16) if int(getHex(self.part, 0x58, 0x5c, True),16) !=0 else False,
            'doubleIndirect' : int(getHex(self.part, 0x5c, 0x60, True),16) if int(getHex(self.part, 0x5c, 0x60, True),16) !=0 else False,
            'tripleIndirect' : int(getHex(self.part, 0x60, 0x64, True),16) if int(getHex(self.part, 0x60, 0x64, True),16) !=0 else False
        }
        self.i_block_list = [self.i_block_dict['directBlock0'], self.i_block_dict['directBlock1'],self.i_block_dict['directBlock2'],self.i_block_dict['directBlock3'],self.i_block_dict['directBlock4'],self.i_block_dict['directBlock5'],self.i_block_dict['directBlock6'],self.i_block_dict['directBlock7'],self.i_block_dict['directBlock8'],self.i_block_dict['directBlock9'],self.i_block_dict['directBlock10'],self.i_block_dict['directBlock11'],self.i_block_dict['singleIndirect'],self.i_block_dict['doubleIndirect'],self.i_block_dict['tripleIndirect']]

        self.reserved_inodes = {0:"Doesn't exist; there is no inode 0.",
                                1:"List of defective blocks.",
                                2:"Root directory.",
                                3:"User Quota",
                                4:"Group Quota",
                                5:"Boot Loader",
                                6:"Undelete Directory",
                                7:"Reserved Group Descriptors inode('resize inode')",
                                8:"Journal inode",
                                9:"The 'exclude' inode, for snapshots(?)",
                                10:'Replica inode, used for some non-upstream feature?'}

