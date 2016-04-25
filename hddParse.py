from partHelp import *
import partData
from ext4.ext4 import ext4
from sys import exit

class hddParse:
    def __init__(self):
        ##
        # MBR partioning:
        #	part 1: 446 (16 bytes)
        ##
        #print("Welcome to James Percival's ext4 filesystem parser")
        #print("Please type 'help' for further information")
        self.currentDir = '/'
        self.parts = []
        self.partsFrame = []
        #iterate the 4 partitions and push the bytes into parts
        #TODO: add ability to parse extended partitions
        hexStr = getLocation(512, 0)
        for x in range(446,446+(16*4),16):
            self.parts.append(getHex(hexStr, x, x+16))
        for index, part in enumerate(self.parts):
            tempPartFrame = {}
            tempPartFrame['start']=int(littleEndian(getHex(part,8,12)), 16)
            tempPartFrame['end']=int(littleEndian(getHex(part,8,12)), 16) + int(littleEndian(getHex(part,12,16)), 16)-1
            tempPartFrame['size']=int(littleEndian(getHex(part,12,16)), 16)
            tempPartFrame['part_type']=partData.partition_type[getHex(part, 4)]
            self.partsFrame.append(tempPartFrame)
        self.filesystem = ext4(self.partsFrame[0])

    def acceptUserInput(self):
        while(1):
            print('>',end='')
            user_input = input()
            self.parseInput(user_input)

    def parseInput(self, user_input):
        user_input = user_input.lstrip()
        user_input_options = user_input.rstrip().split()[1:]
        user_input_options_len = len(user_input_options)
        if user_input == 'help':
            self.userHELP()
        elif user_input[:2] == 'cd':
            self.userCD(user_input_options[0]) if user_input_options_len > 0 else self.userCD()
        elif user_input[:2] == 'ls':
            self.userLS(user_input_options[0:]) if user_input_options_len > 0 else self.userLS([])
        elif user_input[:3] == 'pwd':
            self.userPWD()
        elif user_input[:4] == 'quit':
            self.userQUIT()
        elif user_input[:3] == 'cat':
            self.userCAT(user_input_options[0])
        else:
            print('Bad command given')

    def userHELP(self):
        print('help:\thelp\n\tPrints this message\n')
        print('cd:\tcd [dir]\n\tChange the shell working directory\n')
        print('ls:\tls [-l]\n\tList information about the FILEs(current dir by default)\n')
        print('pwd:\tpwd\n\tPrints the name of the current working directory\n')
        print('quit:\tquit\n\tQuits out of the program\n')

    def userCD(self, dir='/'):
        dir = dir.replace('/', '').replace('\\', '')
        returnCode = self.filesystem.userCD(dir)

        if returnCode == 0:
            self.currentDir += ''+ dir +'/'
        elif returnCode == 1:
            print('filetype operation not supported... your in trouble')
        elif returnCode == 2:
            print('Can not CD into file')
        elif returnCode == 3:
            print('Can not find file')

        if dir == '':
            self.currentDir = '/'

    def userLS(self, user_options):
        long=False
        inode=False
        user_option = ''.join(user_options)
        if 'l' in user_option:
            long = True
        if 'i' in user_option:
            inode = True
        self.filesystem.userLS(long=long, inode=inode)

    def userCAT(self, user_option):
        return_message = self.filesystem.userCAT(user_option)
        print(return_message)

    def userPWD(self):
        print(self.currentDir)

    def userQUIT(self):
        exit(0)

start = hddParse()
start.acceptUserInput()
##self.filesystem is the call to do stuff
