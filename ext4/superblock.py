from partHelp import *
from math import ceil, log
class superblock:
    #TODO:place and create features here
    def s_feature_compat_def(self):
        self.s_feature_compat_dict={'COMPAT_DIR_PREALLOC':False,'COMPAT_IMAGIC_INODES':False,
                                    'COMPAT_HAS_JOURNAL':False,'COMPAT_EXT_ATTR':False,
                                    'COMPAT_RESIZE_INODE':False,'COMPAT_DIR_INDEX':False,
                                    'COMPAT_LAZY_BG':False,'COMPAT_EXCLUDE_INODE':False,
                                    'COMPAT_EXCLUDE_BITMAP':False,'COMPAT_SPARSE_SUPER2':False}

        bitmap = getBitmap(self.s_feature_compat, 10)

        #
        self.s_feature_compat_dict['COMPAT_DIR_PREALLOC'] = bitmap[0]
        #
        self.s_feature_compat_dict['COMPAT_IMAGIC_INODES'] = bitmap[1]
        #
        self.s_feature_compat_dict['COMPAT_HAS_JOURNAL'] = bitmap[2]
        #
        self.s_feature_compat_dict['COMPAT_EXT_ATTR'] = bitmap[3]
        #
        self.s_feature_compat_dict['COMPAT_RESIZE_INODE'] = bitmap[4]
        #
        self.s_feature_compat_dict['COMPAT_DIR_INDEX'] = bitmap[5]
        #
        self.s_feature_compat_dict['COMPAT_LAZY_BG'] = bitmap[6]
        #
        self.s_feature_compat_dict['COMPAT_EXCLUDE_INODE'] = bitmap[7]
        #
        self.s_feature_compat_dict['COMPAT_EXCLUDE_BITMAP'] = bitmap[8]
        #
        self.s_feature_compat_dict['COMPAT_SPARSE_SUPER2'] = bitmap[9]


    def s_feature_incompat_def(self):
    
        self.s_feature_incompat_dict={'INCOMPAT_COMPRESSION':False,'INCOMPAT_FILETYPE':False,
                                    'INCOMPAT_RECOVER':False,'INCOMPAT_JOURNAL_DEV':False,
                                    'INCOMPAT_META_BG':False, 'NOT_USED(0x20)':False,
                                    'INCOMPAT_EXTENTS':False, 'INCOMPAT_64BIT':False,
                                    'INCOMPAT_MMP':False,'INCOMPAT_FLEX_BG':False,
                                    'INCOMPAT_EA_INODE':False, 'NOT_USED(0x800)':False,
                                    'INCOMPAT_DIRDATA':False,'INCOMPAT_CSUM_SEED':False,
                                    'INCOMPAT_LARGEDIR':False,'INCOMPAT_INLINE_DATA':False,
                                    'INCOMPAT_ENCRYPT':False}

        bitmap = getBitmap(self.s_feature_incompat, 17)

        #
        self.s_feature_incompat_dict['INCOMPAT_COMPRESSION'] = bitmap[0]
        #
        self.s_feature_incompat_dict['INCOMPAT_FILETYPE'] = bitmap[1]
        #
        self.s_feature_incompat_dict['INCOMPAT_RECOVER'] = bitmap[2]
        #
        self.s_feature_incompat_dict['INCOMPAT_JOURNAL_DEV'] = bitmap[3]
        #
        self.s_feature_incompat_dict['INCOMPAT_META_BG'] = bitmap[4]
        #
        self.s_feature_incompat_dict['NOT_USED(0x20)'] = bitmap[5]
        #
        self.s_feature_incompat_dict['INCOMPAT_EXTENTS'] = bitmap[6]
        #
        self.s_feature_incompat_dict['INCOMPAT_64BIT'] = bitmap[7]
        #
        self.s_feature_incompat_dict['INCOMPAT_MMP'] = bitmap[8]
        #
        self.s_feature_incompat_dict['INCOMPAT_FLEX_BG'] = bitmap[9]
        #
        self.s_feature_incompat_dict['INCOMPAT_EA_INODE'] = bitmap[10]
        #
        self.s_feature_incompat_dict['NOT_USED(0x800)'] = bitmap[11]
        #
        self.s_feature_incompat_dict['INCOMPAT_DIRDATA'] = bitmap[12]
        #
        self.s_feature_incompat_dict['INCOMPAT_CSUM_SEED'] = bitmap[13]
        #
        self.s_feature_incompat_dict['INCOMPAT_LARGEDIR'] = bitmap[14]
        #
        self.s_feature_incompat_dict['INCOMPAT_INLINE_DATA'] = bitmap[15]
        #
        self.s_feature_incompat_dict['INCOMPAT_ENCRYPT'] = bitmap[16]


    def s_feature_ro_compat_def(self):
        self.s_feature_ro_compat_dict={'RO_COMPAT_SPARSE_SUPER':False,'RO_COMPAT_LARGE_FILE':False,
                                'RO_COMPAT_BTREE_DIR':False,'RO_COMPAT_HUGE_FILE':False,
                                'RO_COMPAT_GDT_CSUM':False,'RO_COMPAT_DIR_NLINK':False,
                                'RO_COMPAT_EXTRA_ISIZE':False,'RO_COMPAT_HAS_SNAPSHOT':False,
                                'RO_COMPAT_QUOTA':False,'RO_COMPAT_BIGALLOC':False,
                                'RO_COMPAT_METADATA_CSUM':False,'RO_COMPAT_REPLICA':False,
                                'RO_COMPAT_READONLY':False}

        bitmap = getBitmap(self.s_feature_ro_compat, 13)

        #
        self.s_feature_ro_compat_dict['RO_COMPAT_SPARSE_SUPER'] = bitmap[0]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_LARGE_FILE'] = bitmap[1]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_BTREE_DIR'] = bitmap[2]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_HUGE_FILE'] = bitmap[3]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_GDT_CSUM'] = bitmap[4]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_DIR_NLINK'] = bitmap[5]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_EXTRA_ISIZE'] = bitmap[6]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_HAS_SNAPSHOT'] = bitmap[7]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_QUOTA'] = bitmap[8]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_BIGALLOC'] = bitmap[9]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_METADATA_CSUM'] = bitmap[10]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_REPLICA'] = bitmap[11]
        #
        self.s_feature_ro_compat_dict['RO_COMPAT_READONLY'] = bitmap[12]


    def __init__(self, part):
        self.superblock = part
        self.part = part


        #####################################################################
        #All entires below have been scraped from the ext4 wiki then changed#
        #####################################################################
        self.s_inodes_count= int(getHex(self.superblock, 0x0, 0x4, True), 16)#Total inode count.
        self.s_blocks_count_lo= int(getHex(self.superblock, 0x4, 0x8, True), 16)#Total block count.
        self.s_r_blocks_count_lo= int(getHex(self.superblock, 0x8, 0xc, True), 16)#This number of blocks can only be allocated by the super-user.
        self.s_free_blocks_count_lo= int(getHex(self.superblock, 0xC, 0x10, True), 16)#Free block count.
        self.s_free_inodes_count= int(getHex(self.superblock, 0x10, 0x14, True), 16)#Free inode count.
        self.s_first_data_block= int(getHex(self.superblock, 0x14, 0x18, True), 16)#First data block.  This must be at least 1 for 1k-block filesystems and is typically 0 for all other block sizes.
        self.s_log_block_size= int(getHex(self.superblock, 0x18, 0x1c, True), 16)#Block size is 2 ^ (10 + s_log_block_size).
        self.s_log_cluster_size= int(getHex(self.superblock, 0x1C, 0x20, True), 16)#Cluster size is (2 ^ s_log_cluster_size) blocks if bigalloc is enabled, zero otherwise.
        self.s_blocks_per_group= int(getHex(self.superblock, 0x20, 0x24, True), 16)#Blocks per group.
        self.s_clusters_per_group= int(getHex(self.superblock, 0x24, 0x28, True), 16)#Clusters per group, if bigalloc is enabled.
        self.s_inodes_per_group= int(getHex(self.superblock, 0x28, 0x2c, True), 16)#Inodes per group.
        self.s_mtime= int(getHex(self.superblock, 0x2C, 0x30, True), 16)#Mount time, in seconds since the epoch.
        self.s_wtime= int(getHex(self.superblock, 0x30, 0x34, True), 16)#Write time, in seconds since the epoch.
        self.s_mnt_count= int(getHex(self.superblock, 0x34, 0x36, True), 16)#Number of mounts since the last fsck.
        self.s_max_mnt_count= int(getHex(self.superblock, 0x36, 0x38, True), 16)#Number of mounts beyond which a fsck is needed.
        self.s_magic= int(getHex(self.superblock, 0x38, 0x3a, True), 16)#Magic signature, 0xEF53
        self.s_state= int(getHex(self.superblock, 0x3A, 0x3c, True), 16)#None
        self.s_errors= int(getHex(self.superblock, 0x3C, 0x3e, True), 16)#None
        self.s_minor_rev_level= int(getHex(self.superblock, 0x3E, 0x40, True), 16)#Minor revision level.
        self.s_lastcheck= int(getHex(self.superblock, 0x40, 0x44, True), 16)#Time of last check, in seconds since the epoch.
        self.s_checkinterval= int(getHex(self.superblock, 0x44, 0x48, True), 16)#Maximum time between checks, in seconds.
        self.s_creator_os= int(getHex(self.superblock, 0x48, 0x4c, True), 16)#None
        self.s_rev_level= int(getHex(self.superblock, 0x4C, 0x50, True), 16)#None
        self.s_def_resuid= int(getHex(self.superblock, 0x50, 0x52, True), 16)#Default uid for reserved blocks.
        self.s_def_resgid= int(getHex(self.superblock, 0x52, 0x54, True), 16)#Default gid for reserved blocks.
        self.s_first_ino= int(getHex(self.superblock, 0x54, 0x58, True), 16)#First non-reserved inode.
        self.s_inode_size= int(getHex(self.superblock, 0x58, 0x5a, True), 16)#Size of inode structure, in bytes.
        self.s_block_group_nr= int(getHex(self.superblock, 0x5A, 0x5c, True), 16)#Block group # of this superblock.
        self.s_feature_compat= int(getHex(self.superblock, 0x5C, 0x60, True), 16)#None
        self.s_feature_incompat= int(getHex(self.superblock, 0x60, 0x64, True), 16)#None
        self.s_feature_ro_compat= int(getHex(self.superblock, 0x64, 0x68, True), 16)#None
        self.s_uuid= int(getHex(self.superblock, 0x68, 0x78, False), 16)#128-bit UUID for volume. [16]
        self.s_volume_name= int(getHex(self.superblock, 0x78, 0x88, False), 16)#Volume label. [16]
        self.s_last_mounted= int(getHex(self.superblock, 0x88, 0xc8, False), 16)#Directory where filesystem was last mounted. [64]
        self.s_algorithm_usage_bitmap= int(getHex(self.superblock, 0xC8 , 0xcc, True), 16)#For compression (Not used in e2fsprogs/Linux)
        self.s_prealloc_blocks= int(getHex(self.superblock, 0xCC, 0xcd, False), 16)## of blocks to try to preallocate for ... files? (Not used in e2fsprogs/Linux)
        self.s_prealloc_dir_blocks= int(getHex(self.superblock, 0xCD, 0xce, False), 16)## of blocks to preallocate for directories. (Not used in e2fsprogs/Linux)
        self.s_reserved_gdt_blocks= int(getHex(self.superblock, 0xCE, 0xd0, True), 16)#Number of reserved GDT entries for future filesystem expansion.
        self.s_journal_uuid= int(getHex(self.superblock, 0xD0, 0xe0, False), 16)#UUID of journal superblock [16]
        self.s_journal_inum= int(getHex(self.superblock, 0xE0, 0xe4, True), 16)#inode number of journal file.
        self.s_journal_dev= int(getHex(self.superblock, 0xE4, 0xe8, True), 16)#Device number of journal file, if the external journal feature flag is set.
        self.s_last_orphan= int(getHex(self.superblock, 0xE8, 0xec, True), 16)#Start of list of orphaned inodes to delete.
        self.s_hash_seed= int(getHex(self.superblock, 0xEC, 0xfc, True), 16)#HTREE hash seed.  [4]
        self.s_def_hash_version= int(getHex(self.superblock, 0xFC, 0xfd, False), 16)#None
        self.s_jnl_backup_type= int(getHex(self.superblock, 0xFD, 0xfe, False), 16)#None
        self.s_desc_size= int(getHex(self.superblock, 0xFE, 0x100, True), 16)#Size of group descriptors, in bytes, if the 64bit incompat feature flag is set.
        self.s_default_mount_opts= int(getHex(self.superblock, 0x100, 0x104, True), 16)#None
        self.s_first_meta_bg= int(getHex(self.superblock, 0x104, 0x108, True), 16)#First metablock block group, if the meta_bg feature is enabled.
        self.s_mkfs_time= int(getHex(self.superblock, 0x108, 0x10c, True), 16)#When the filesystem was created, in seconds since the epoch.
        self.s_jnl_blocks= int(getHex(self.superblock, 0x10C, 0x150, True), 16)#None [17]
        self.s_blocks_count_hi= int(getHex(self.superblock, 0x150, 0x154, True), 16)#High 32-bits of the block count.
        self.s_r_blocks_count_hi= int(getHex(self.superblock, 0x154, 0x158, True), 16)#High 32-bits of the reserved block count.
        self.s_free_blocks_count_hi= int(getHex(self.superblock, 0x158, 0x15c, True), 16)#High 32-bits of the free block count.
        self.s_min_extra_isize= int(getHex(self.superblock, 0x15C, 0x15e, True), 16)#All inodes have at least # bytes.
        self.s_want_extra_isize= int(getHex(self.superblock, 0x15E, 0x160, True), 16)#New inodes should reserve # bytes.
        self.s_flags= int(getHex(self.superblock, 0x160, 0x164, True), 16)#None
        self.s_raid_stride= int(getHex(self.superblock, 0x164, 0x166, True), 16)#RAID stride.  This is the number of logical blocks read from or written to the disk before moving to the next disk.  This affects the placement of filesystem metadata, which will hopefully make RAID storage faster.
        self.s_mmp_interval= int(getHex(self.superblock, 0x166, 0x168, True), 16)## seconds to wait in multi-mount prevention (MMP) checking.  In theory, MMP is a mechanism to record in the superblock which host and device have mounted the filesystem, in order to prevent multiple mounts.  This feature does not seem to be implemented...
        self.s_mmp_block= int(getHex(self.superblock, 0x168, 0x170, True), 16)#Block # for multi-mount protection data.
        self.s_raid_stripe_width= int(getHex(self.superblock, 0x170, 0x174, True), 16)#RAID stripe width.  This is the number of logical blocks read from or written to the disk before coming back to the current disk.  This is used by the block allocator to try to reduce the number of read-modify-write operations in a RAID5/6.
        self.s_log_groups_per_flex= int(getHex(self.superblock, 0x174, 0x175, False), 16)#None
        self.s_checksum_type= int(getHex(self.superblock, 0x175, 0x176, False), 16)#Metadata checksum algorithm type.  The only valid value is 1 (crc32c).
        self.s_reserved_pad= int(getHex(self.superblock, 0x176, 0x178, True), 16)#
        self.s_kbytes_written= int(getHex(self.superblock, 0x178, 0x180, True), 16)#Number of KiB written to this filesystem over its lifetime.
        self.s_snapshot_inum= int(getHex(self.superblock, 0x180, 0x184, True), 16)#inode number of active snapshot. (Not used in e2fsprogs/Linux.)
        self.s_snapshot_id= int(getHex(self.superblock, 0x184, 0x188, True), 16)#Sequential ID of active snapshot. (Not used in e2fsprogs/Linux.)
        self.s_snapshot_r_blocks_count= int(getHex(self.superblock, 0x188, 0x190, True), 16)#Number of blocks reserved for active snapshot's future use. (Not used in e2fsprogs/Linux.)
        self.s_snapshot_list= int(getHex(self.superblock, 0x190, 0x194, True), 16)#inode number of the head of the on-disk snapshot list. (Not used in e2fsprogs/Linux.)
        self.s_error_count= int(getHex(self.superblock, 0x194, 0x198, True), 16)#Number of errors seen.
        self.s_first_error_time= int(getHex(self.superblock, 0x198, 0x19c, True), 16)#First time an error happened, in seconds since the epoch.
        self.s_first_error_ino= int(getHex(self.superblock, 0x19C, 0x1a0, True), 16)#inode involved in first error.
        self.s_first_error_block= int(getHex(self.superblock, 0x1A0, 0x1a8, True), 16)#Number of block involved of first error.
        self.s_first_error_func= int(getHex(self.superblock, 0x1A8, 0x1c8, False), 16)#Name of function where the error happened. [32]
        self.s_first_error_line= int(getHex(self.superblock, 0x1C8, 0x1cc, True), 16)#Line number where error happened.
        self.s_last_error_time= int(getHex(self.superblock, 0x1CC, 0x1d0, True), 16)#Time of most recent error, in seconds since the epoch.
        self.s_last_error_ino= int(getHex(self.superblock, 0x1D0, 0x1d4, True), 16)#inode involved in most recent error.
        self.s_last_error_line= int(getHex(self.superblock, 0x1D4, 0x1d8, True), 16)#Line number where most recent error happened.
        self.s_last_error_block= int(getHex(self.superblock, 0x1D8, 0x1e0, True), 16)#Number of block involved in most recent error.
        self.s_last_error_func= int(getHex(self.superblock, 0x1E0, 0x200, False), 16)#Name of function where the most recent error happened. [32]
        self.s_mount_opts= int(getHex(self.superblock, 0x200, 0x240, False), 16)#ASCIIZ string of mount options. [64]
        self.s_usr_quota_inum= int(getHex(self.superblock, 0x240, 0x244, True), 16)#None
        self.s_grp_quota_inum= int(getHex(self.superblock, 0x244, 0x248, True), 16)#None
        self.s_overhead_blocks= int(getHex(self.superblock, 0x248, 0x24c, True), 16)#Overhead blocks/clusters in fs. (Huh? This field is always zero, which means that the kernel calculates it dynamically.)
        self.s_backup_bgs= int(getHex(self.superblock, 0x24C, 0x254, True), 16)#Block groups containing superblock backups (if sparse_super2) [2]
        self.s_encrypt_algos= int(getHex(self.superblock, 0x254, 0x258, False), 16)#None
        self.s_encrypt_pw_salt= int(getHex(self.superblock, 0x258, 0x268, False), 16)#Salt for the string2key algorithm for encryption.
        self.s_lpf_ino= int(getHex(self.superblock, 0x268, 0x26c, True), 16)#Inode number of lost+found
        self.s_checksum_seed= int(getHex(self.superblock, 0x26C, 0x270, True), 16)#Checksum seed used for metadata_csum calculations.  This value is crc32c(~0, $orig_fs_uuid).
        self.s_reserved= int(getHex(self.superblock, 0x270, 0x3fc, True), 16)#Padding to the end of the block.
        self.s_checksum= int(getHex(self.superblock, 0x3FC, 0x400, True), 16)#Superblock checksum.

        self.s_feature_compat_def()
        self.s_feature_incompat_def()
        self.s_feature_ro_compat_def()

        ##MY VARS##
        self.desc_block_num=int(self.s_blocks_count_lo+(self.s_blocks_count_hi<<32) / self.s_blocks_per_group +1) if self.s_feature_incompat_dict['INCOMPAT_64BIT'] else int(self.s_blocks_count_lo / self.s_blocks_per_group +1)
        #if sparse_super is on
        self.desc_blocks_with_super = set([0,1]+[3**x for x in range(1,int(ceil(log(self.desc_block_num,3))))] +\
            [5**x for x in range(1,int(ceil(log(self.desc_block_num,5))))] + \
            [7**x for x in range(1,int(ceil(log(self.desc_block_num,7))))])
        self.block_size = 1024 << self.s_log_block_size
        #if flex_bg is enabled
        self.groups_in_flex = 2 ** self.s_log_groups_per_flex

        print('s_feature_compat')
        for x in self.s_feature_compat_dict:
            if self.s_feature_compat_dict[x] == True:
                print('\t'+x)

        print('s_feature_compat_dict')
        for x in self.s_feature_incompat_dict:
            if self.s_feature_incompat_dict[x] == True:
                print('\t'+x)


        print('s_feature_ro_compat_dict')
        for x in self.s_feature_ro_compat_dict:
            if self.s_feature_ro_compat_dict[x] == True:
                print('\t'+x)

        
