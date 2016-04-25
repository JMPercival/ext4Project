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



import tkinter
import tkinter.ttk as ttk
class frontend(tkinter.Frame):
    def __init__(self, parent, fs):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.fs = fs

        self.initUI()

    ##UI Controls##
    def selection(self):
        try:
            pass
        except:
            pass

    def onExit(self):
        self.quit()

    
    ##UI Setup##
    def setupMenubar(self):
        menubar = tkinter.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = tkinter.Menu(menubar)
        fileMenu.add_command(label='exit', command=self.onExit)
        menubar.add_cascade(label='file',menu=fileMenu)

    def setupEntry(self):
        self.textbox = tkinter.Entry(self.parent)

    def setupListbox(self):
        self.listbox = tkinter.Listbox(self.parent)
        for dir in fs.filesystem.current_dir_list:
            self.listbox.insert(tkinter.END, dir)
        
    def setupSelectButton(self):
        self.selectButton = tkinter.Button(self.parent, text='Select', underline=0, command=self.selection)

    def setupTreeview(self):
        self.tree = ttk.Treeview(self.parent)
        self.tree['columns'] = ('name', 'permission')
        self.tree.column('name', width=150)
        self.tree.column('permission', width=100)
        self.tree.heading('name', text='Name')
        self.tree.heading('permission', text='Permissions')

        for dir in fs.filesystem.userLS():
            self.tree.insert("", tkinter.END, values=[dir['name'], dir['permission']])
        

        
    def setupPacks(self):
        self.textbox.pack()
        #self.listbox.pack(fill=tkinter.BOTH)
        self.tree.pack()
        self.selectButton.pack()

    def initUI(self):
        self.parent.title("EXT4 File Viewer")
        self.setupMenubar()
        self.setupEntry()
        #self.setupListbox()
        self.setupSelectButton()
        self.setupTreeview()
        self.setupPacks()

    ##General Functions##
    def addListToTree(self, dir_list):
        for dir in dirs:
            self.listbox.insert()



if __name__ == '__main__':
    fs = hddParse()
    master=tkinter.Tk()
    master.geometry('250x150+300+300')
    app = frontend(master, fs)
    master.mainloop()
##self.filesystem is the call to do stuff
