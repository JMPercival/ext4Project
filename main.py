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
import random
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

    def cat_window_delete(self):
        self.cat_window_up = 0
        self.slave_window.destroy()


    def onExit(self):
        self.quit()

    def reload_tree(self):
        self.tree.destroy()
        self.setupTreeview()
        self.tree.pack(fill=tkinter.BOTH, expand=True, side=tkinter.TOP)

    ##UI Setup##
    def setupMenubar(self):
        menubar = tkinter.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = tkinter.Menu(menubar)
        fileMenu.add_command(label='Exit', command=self.onExit)
        menubar.add_cascade(label='File',menu=fileMenu)
        
        self.UID_checkbox = tkinter.BooleanVar()
        self.GID_checkbox = tkinter.BooleanVar()
        self.size_checkbox = tkinter.BooleanVar()
        self.access_time_checkbox = tkinter.BooleanVar()
        self.permission_checkbox = tkinter.BooleanVar()

        columnMenu = tkinter.Menu(menubar)
        columnMenu.add_checkbutton(label='Permissions', onvalue=True, offvalue=False, variable=self.permission_checkbox)
        columnMenu.add_checkbutton(label='UID', onvalue=True, offvalue=False, variable=self.UID_checkbox)
        columnMenu.add_checkbutton(label='GID', onvalue=True, offvalue=False, variable=self.GID_checkbox)
        columnMenu.add_checkbutton(label='Size', onvalue=True, offvalue=False, variable=self.size_checkbox)
        columnMenu.add_checkbutton(label='Access_Time', onvalue=True, offvalue=False, variable=self.access_time_checkbox)
        columnMenu.add_command(label='Reload Tree', command=self.reload_tree)
        menubar.add_cascade(label='Columns', menu=columnMenu)


    def setupEntry(self):
        self.textbox = tkinter.Entry(self.parent)

    def setupListbox(self):
        self.listbox = tkinter.Listbox(self.parent)
        for dir in fs.filesystem.current_dir_list:
            self.listbox.insert(tkinter.END, dir)
        
    def setupSelectButton(self):
        self.selectButton = tkinter.Button(self.parent, text='Select', underline=0, command=self.selection)

    def setupTreeview(self):
        self.tree = ttk.Treeview(self.parent, yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set)
        self.tree.bind('<<TreeviewOpen>>', self.treeOpen)
        self.tree.bind('<<TreeviewClose>>', self.treeClose)

        self.tree.tag_configure('greenTag', background = 'green')
        self.tree.tag_configure('blueTag', background = 'blue')
        self.tree.tag_configure('redTag', background = 'red')
        self.tree.tag_configure('orangeTag', background = 'orange')

        self.tree['columns'] = ('name', 'inode', 'filetype')
        if self.permission_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('permission',)
        if self.UID_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('uid',)
        if self.GID_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('gid',)
        if self.size_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('size',)
        if self.access_time_checkbox.get():
           self.tree['columns'] = self.tree['columns'] + ('access_time',) 

        self.tree.column('name', width=150)
        self.tree.column('inode', width=50)
        self.tree.column('filetype',width=75)

        self.tree.heading('name', text='Name')
        self.tree.heading('inode', text='Inode')
        self.tree.heading('filetype', text='Filetype')

        if self.permission_checkbox.get():
            self.file_values_to_show += ['permission']
            self.tree.column('permission', width=100)
            self.tree.heading('permission', text='Permissions')

        if self.UID_checkbox.get():
            self.file_values_to_show += ['']
            self.tree.column('permission', width=100)
            self.tree.heading('permission', text='Permissions')

        if self.GID_checkbox.get():
        if self.size_checkbox.get():
        if self.access_time_checkbox.get():


        self.scrollbary.config(command=self.tree.yview)
        self.scrollbarx.config(command=self.tree.xview)



        tag_to_use = 'greenTag'
        for dir in fs.filesystem.userLS():
            if dir['inode']==2:
                continue
            self.addChildToTree("", tkinter.END, dir, tag_to_use)

        self.depth = 1
        for parent_id in self.tree.get_children():
            parent_dict = self.tree.set(parent_id)
            if parent_dict['inode'] == '2' or parent_dict['filetype'] != 'Directory':
                continue
            tag_to_use = 'orangeTag'
            children_list = self.fs.filesystem.userLoadDir(parent_dict['inode'])
            for child_dict in children_list:
                if child_dict['inode'] == int(parent_dict['inode']) or child_dict['inode'] == 2:
                    continue
                self.addChildToTree(parent_id, tkinter.END, child_dict, tag_to_use)

    def setupScrollBars(self):
        self.scrollbary = tkinter.Scrollbar(self.parent, orient=tkinter.VERTICAL)
        self.scrollbarx = tkinter.Scrollbar(self.parent, orient=tkinter.HORIZONTAL)

    def setupPacks(self):
        #self.textbox.pack()
        #self.listbox.pack(fill=tkinter.BOTH)
        self.scrollbary.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.scrollbarx.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.tree.pack(fill=tkinter.BOTH, expand=True, side=tkinter.TOP)
        #self.selectButton.pack()

    def initUI(self):
        self.file_values_to_show = ['name', 'inode', 'filetype']
        self.depth = 0
        self.cat_window_up = 0
        self.parent.title("EXT4 File Viewer")
        self.setupMenubar()
        self.setupEntry()
        #self.setupListbox()
        self.setupSelectButton()
        self.setupScrollBars()
        self.setupTreeview()
        self.setupPacks()

    def cat_window(self, name, info):
        if self.cat_window_up == 0:
            self.slave_window = tkinter.Toplevel(self)
            self.slave_window.protocol("WM_DELETE_WINDOW", self.cat_window_delete)
            self.slave_window.wm_title("Notebook")
            self.notebook = ttk.Notebook(self.slave_window)
            self.notebook.pack()
            self.cat_window_up = 1

        print(self.notebook)
        
        f1 = ttk.Frame(self.notebook)
        self.notebook.add(f1, text = name)
        self.notebook.select(f1)
        text = tkinter.Text(f1)
        text.insert(tkinter.INSERT, info)
        text.pack()

    ##General Functions##
    def setupNewTreeTag(self):
        randList = [chr(x) for x in range(0x41, 0x5a)]
        randTagName = ''.join([random.choice(randList) for x in range(16)])
        self.tree.tag_configure(randTagName, background='#{:06x}'.format(random.randint(0x009999, 0x00ffff)))
        return randTagName

    def addChildToTree(self, id, index, dir, tag_to_use):
        values = []
        dir['name'] = (' '*3*self.depth) + dir['name']
        for value in self.file_values_to_show:
            values.append(dir[value])
        self.tree.insert(id, index, values=values, tags=(tag_to_use))

    def treeOpen(self, event):
        selected_item = self.tree.selection()[0]
        selected_item_dict = self.tree.set(selected_item)
        if selected_item_dict['filetype'] != 'Directory':
            self.cat_window(selected_item_dict['name'], self.fs.filesystem.userCAT(selected_item_dict['inode']))
            self.tree.item(selected_item, open=False)
        else:
            for parent_id in self.tree.get_children(selected_item):
                self.depth = self.getDepth(parent_id) + 1
                parent_dict = self.tree.set(parent_id)
                if parent_dict['inode'] == '2' or parent_dict['filetype'] != 'Directory':
                    continue

                if self.tree.get_children(parent_id) != ():
                    print('continuing')
                    continue
                print(self.tree.get_children(parent_id))

                children_list = self.fs.filesystem.userLoadDir(parent_dict['inode'])
                tag_to_use = self.setupNewTreeTag()
                for child_dict in children_list:
                    if child_dict['inode'] == int(parent_dict['inode']) or child_dict['inode'] == 2:
                        continue
                self.addChildToTree(parent_id, tkinter.END, child_dict, tag_to_use)

    def getDepth(self, node_id):
        depth = 0
        check_parent = self.tree.parent(node_id)
        while check_parent != '':
            check_parent = self.tree.parent(check_parent)
            depth += 1
        return depth

    def treeClose(self, event):
        print('tree close')


    def addListToTree(self, dir_list):
        for dir in dirs:
            self.listbox.insert()



if __name__ == '__main__':
    fs = hddParse()
    master=tkinter.Tk()
    #master.geometry('250x150+300+300')
    app = frontend(master, fs)
    master.mainloop()
##self.filesystem is the call to do stuff
