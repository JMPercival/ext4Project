from partHelp import *

#takes in the part we need and the superblock
class directory:
    def __init__(self, part, superblock):
        self.part = part
        self.superblock = superblock
        self.inode= int(getHex(self.part, 0x0, 0x4, True),16)#Inode
        self.rec_len= int(getHex(self.part, 0x4, 0x6, True),16)#Total size of this entry (Including all subfields)
        if superblock.s_feature_incompat_dict['INCOMPAT_FILETYPE'] == True:
            self.name_len= int(getHex(self.part, 0x6, 0x7, True),16)#Name Length least-significant 8 bits
            self.file_type= int(getHex(self.part, 0x7, 0x8, True),16)#Type indicator (only if the feature bit for "directory entries have file type byte" is set, else this is the most-significant 8 bits of the Name Length)
        else:
            self.name_len= int(getHex(self.part, 0x6, 0x8, True),16) #Name Length
        self.name= getHex(self.part, 0x8, 0x8 + self.name_len, False)#Name characters

        self.decoded_name = ''.join([chr(int(self.name[c:c+2], 16)) for c in range(0,len(self.name),2)])


    def isFiletype(self):
        return self.superblock.s_feature_incompat_dict['INCOMPAT_FILETYPE']

    def __hash__(self):
        return hash((self.name,self.inode))
    def __eq__(self, other):
        return (self.name, self.inode) == (other.name, other.inode)
