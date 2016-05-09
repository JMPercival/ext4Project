from partHelp import *
import partData
from ext4.ext4 import ext4
from sys import exit

class hddParse:
    def __init__(self, filesystem_to_use, partition_to_use):
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
        hexStr = getLocation(512, 0, filesystem_to_use)
        for x in range(446,446+(16*4),16):
            self.parts.append(getHex(hexStr, x, x+16))
        for index, part in enumerate(self.parts):
            tempPartFrame = {}
            tempPartFrame['start']=int(littleEndian(getHex(part,8,12)), 16)
            tempPartFrame['end']=int(littleEndian(getHex(part,8,12)), 16) + int(littleEndian(getHex(part,12,16)), 16)-1
            tempPartFrame['size']=int(littleEndian(getHex(part,12,16)), 16)
            tempPartFrame['part_type']=partData.partition_type[getHex(part, 4)]
            self.partsFrame.append(tempPartFrame)

        self.filesystem = ext4(self.partsFrame[partition_to_use], filesystem_to_use)



import tkinter
import tkinter.ttk as ttk
import random
class frontend(tkinter.Frame):
    def __init__(self, parent):
        #temp values til it can be set in box
        self.filesystem_to_use = 'my_drive'
        self.partition_to_use = 0
        self.fs = hddParse(self.filesystem_to_use, self.partition_to_use)
        tkinter.Frame.__init__(self, parent)
        self.parent = parent

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

    def reloadFilesystem(self):
        self.fs = hddParse(self.filesystem_to_use, self.partition_to_use)
        self.reload_tree()

    def getNewFilesystemSettings(self):
        self.filesystem_to_use = self.filesystem_entry.get()
        self.partition_to_use = int(self.partition_to_use_internal.get())
        self.filesystem_config_slave_window.destroy()
        
        self.reloadFilesystem()

    def configureFilesystem(self):
        self.filesystem_config_slave_window = tkinter.Toplevel(self)
        self.filesystem_config_slave_window.wm_title("Filesystem Config")

        self.filesystem_entry = tkinter.Entry(self.filesystem_config_slave_window)
        self.filesystem_entry.insert(tkinter.INSERT, self.filesystem_to_use)

        self.partition_to_use_internal = tkinter.StringVar()
        self.partition_to_use_internal.set(self.partition_to_use)
        self.dropdown = tkinter.OptionMenu(self.filesystem_config_slave_window,self.partition_to_use_internal,'0','1','2','3')

        filesystem_label = tkinter.Label(self.filesystem_config_slave_window, text="Filesystem to use:")
        dropdown_label = tkinter.Label(self.filesystem_config_slave_window, text="Partition to use:")

        done_button = tkinter.Button(self.filesystem_config_slave_window, text = 'Done', command=self.getNewFilesystemSettings)

        filesystem_label.pack(side=tkinter.TOP, anchor=tkinter.W)
        self.filesystem_entry.pack(side=tkinter.TOP, anchor=tkinter.W)

        dropdown_label.pack(side=tkinter.TOP, anchor=tkinter.W)
        self.dropdown.pack(side=tkinter.TOP, anchor=tkinter.W)

        done_button.pack(side=tkinter.TOP, anchor=tkinter.W)

    def detailSuperblockWindow(self):
        self.superblock_detail_slave_window = tkinter.Toplevel(self)
        self.superblock_detail_slave_window.wm_title("Superblock Detail")

        text = tkinter.Text(self.superblock_detail_slave_window)

        info = self.fs.filesystem.getSuperblockVars()

        text.insert(tkinter.INSERT, info)
        text.pack(fill=tkinter.BOTH, expand=True)


    def detailGroupDescWindow(self):
        self.group_desc_detail_slave_window = tkinter.Toplevel(self)
        self.group_desc_detail_slave_window.wm_title("Superblock Detail")

        text = tkinter.Text(self.group_desc_detail_slave_window)

        info = self.fs.filesystem.getGroupDescVars()
        
        text.insert(tkinter.INSERT, info)
        text.pack(fill=tkinter.BOTH, expand=True)

    ##UI Setup##
    def setupMenubar(self):
        menubar = tkinter.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = tkinter.Menu(menubar)
        fileMenu.add_command(label='Exit', command=self.onExit)
        menubar.add_cascade(label='File',menu=fileMenu)

        configMenu = tkinter.Menu(menubar)
        configMenu.add_command(label='Filesystem', command=self.configureFilesystem)
        menubar.add_cascade(label='Configure', menu=configMenu)
        
        self.UID_checkbox = tkinter.BooleanVar()
        self.GID_checkbox = tkinter.BooleanVar()
        self.size_checkbox = tkinter.BooleanVar()
        self.access_time_checkbox = tkinter.BooleanVar()
        self.permission_checkbox = tkinter.BooleanVar()
        self.change_time_checkbox = tkinter.BooleanVar()
        self.modify_time_checkbox = tkinter.BooleanVar()
        self.delete_time_checkbox = tkinter.BooleanVar()
        self.creation_time_checkbox = tkinter.BooleanVar()
        self.file_acl_checkbox = tkinter.BooleanVar()
        self.checksum_checkbox = tkinter.BooleanVar()
        self.flags_checkbox = tkinter.BooleanVar()
        self.links_count_checkbox = tkinter.BooleanVar()
        self.blocks_count_checkbox = tkinter.BooleanVar()
        self.mode_checkbox = tkinter.BooleanVar()

        columnMenu = tkinter.Menu(menubar)
        columnMenu.add_checkbutton(label='Permissions', onvalue=True, offvalue=False, variable=self.permission_checkbox)
        columnMenu.add_checkbutton(label='UID', onvalue=True, offvalue=False, variable=self.UID_checkbox)
        columnMenu.add_checkbutton(label='GID', onvalue=True, offvalue=False, variable=self.GID_checkbox)
        columnMenu.add_checkbutton(label='Size', onvalue=True, offvalue=False, variable=self.size_checkbox)
        columnMenu.add_checkbutton(label='Access_Time', onvalue=True, offvalue=False, variable=self.access_time_checkbox)
        columnMenu.add_checkbutton(label='change_time', onvalue=True, offvalue=False, variable=self.change_time_checkbox)
        columnMenu.add_checkbutton(label='modify_time', onvalue=True, offvalue=False, variable=self.modify_time_checkbox)
        columnMenu.add_checkbutton(label='delete_time', onvalue=True, offvalue=False, variable=self.delete_time_checkbox)
        columnMenu.add_checkbutton(label='creation_time', onvalue=True, offvalue=False, variable=self.creation_time_checkbox)
        columnMenu.add_checkbutton(label='file_acl', onvalue=True, offvalue=False, variable=self.file_acl_checkbox)
        columnMenu.add_checkbutton(label='checksum', onvalue=True, offvalue=False, variable=self.checksum_checkbox)
        columnMenu.add_checkbutton(label='flags', onvalue=True, offvalue=False, variable=self.flags_checkbox)
        columnMenu.add_checkbutton(label='links_count', onvalue=True, offvalue=False, variable=self.links_count_checkbox)
        columnMenu.add_checkbutton(label='blocks_count', onvalue=True, offvalue=False, variable=self.blocks_count_checkbox)
        columnMenu.add_checkbutton(label='mode', onvalue=True, offvalue=False, variable=self.mode_checkbox)
        columnMenu.add_command(label='Apply New Columns', command=self.reload_tree)
        menubar.add_cascade(label='Columns', menu=columnMenu)

        detailMenu = tkinter.Menu(menubar)
        detailMenu.add_command(label='Superblock', command=self.detailSuperblockWindow)
        detailMenu.add_command(label='Group Descriptors', command=self.detailGroupDescWindow)
        menubar.add_cascade(label='Details', menu=detailMenu)

    def setupEntry(self):
        self.textbox = tkinter.Entry(self.parent)

    def setupListbox(self):
        self.listbox = tkinter.Listbox(self.parent)
        for dir in self.fs.filesystem.current_dir_list:
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
        if self.change_time_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('change_time',) 
        if self.modify_time_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('modify_time',)
        if self.delete_time_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('delete_time',)
        if self.creation_time_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('creation_time',)
        if self.file_acl_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('file_acl',)
        if self.checksum_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('checksum',)
        if self.flags_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('flags',)
        if self.links_count_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('links_count',)
        if self.blocks_count_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('blocks_count',)
        if self.mode_checkbox.get():
            self.tree['columns'] = self.tree['columns'] + ('mode',)

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
            self.file_values_to_show += ['uid']
            self.tree.column('uid', width=100)
            self.tree.heading('uid', text='UID')
        if self.GID_checkbox.get():
            self.file_values_to_show += ['gid']
            self.tree.column('gid', width=100)
            self.tree.heading('gid', text='GID')
        if self.size_checkbox.get():
            self.file_values_to_show += ['size']
            self.tree.column('size', width=100)
            self.tree.heading('size', text='Size')
        if self.access_time_checkbox.get():
            self.file_values_to_show += ['access_time']
            self.tree.column('access_time', width=100)
            self.tree.heading('access_time', text='Access_Time')
        if self.change_time_checkbox.get():
            self.file_values_to_show += ['change_time']
            self.tree.column('change_time', width=100)
            self.tree.heading('change_time', text='Change_Time')
        if self.modify_time_checkbox.get():
            self.file_values_to_show += ['modify_time']
            self.tree.column('modify_time', width=100)
            self.tree.heading('modify_time', text='Modify_Time')
        if self.delete_time_checkbox.get():
            self.file_values_to_show += ['delete_time']
            self.tree.column('delete_time', width=100)
            self.tree.heading('delete_time', text='Delete_Time')
        if self.creation_time_checkbox.get():
            self.file_values_to_show += ['creation_time']
            self.tree.column('creation_time', width=100)
            self.tree.heading('creation_time', text='Creation_Time')
        if self.file_acl_checkbox.get():
            self.file_values_to_show += ['file_acl']
            self.tree.column('file_acl', width=100)
            self.tree.heading('file_acl', text='File_ACL')
        if self.checksum_checkbox.get():
            self.file_values_to_show += ['checksum']
            self.tree.column('checksum', width=100)
            self.tree.heading('checksum', text='Checksum')
        if self.flags_checkbox.get():
            self.file_values_to_show += ['flags']
            self.tree.column('flags', width=100)
            self.tree.heading('flags', text='Flags')
        if self.links_count_checkbox.get():
            self.file_values_to_show += ['links_count']
            self.tree.column('links_count', width=100)
            self.tree.heading('links_count', text='Links_Count')
        if self.blocks_count_checkbox.get():
            self.file_values_to_show += ['blocks_count']
            self.tree.column('blocks_count', width=100)
            self.tree.heading('blocks_count', text='Blocks_Count')
        if self.mode_checkbox.get():
            self.file_values_to_show += ['mode']
            self.tree.column('mode', width=100)
            self.tree.heading('mode', text='Mode')

        self.scrollbary.config(command=self.tree.yview)
        self.scrollbarx.config(command=self.tree.xview)
        
        self.depth = 0
        tag_to_use = 'greenTag'
        for dir in self.fs.filesystem.userLS():
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
        self.filesystem_to_use = 'my_drive'
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
    master=tkinter.Tk()
    #master.geometry('250x150+300+300')
    app = frontend(master)
    master.mainloop()
##self.filesystem is the call to do stuff
