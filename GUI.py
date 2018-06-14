from Tkinter import *
import ttk
from server import *
import os

class GUI(object):
    def __init__(self):
        self.server = Server()
        self.server.run_thread()
        self.ip_list = []# self.server.get_ip_list()

        self.files = []
        self.folders = []
        self.tree = []

        root = Tk()
        up_frame = Frame(root)
        up_frame.pack()

        bottomframe = Frame(root)
        bottomframe.pack( side = BOTTOM)

        bottom_left_frame=Frame(bottomframe)
        bottom_left_frame.pack( side = LEFT)

        self.tree_frame=Frame(bottomframe)
        self.tree_frame.pack( side = RIGHT)

        self.ips=ttk.Combobox(up_frame,postcommand=self.update_ips , width=80, state='readonly')# postcommand=self.update_ips
        self.ips.pack()
        # Thread(target=self.update_ips).start()

        self.path = []

        self.scrollbar = Scrollbar(self.tree_frame)
        self.scrollbar.pack(side=LEFT, fill=Y)

        self.tree_list = Listbox(self.tree_frame, yscrollcommand=self.scrollbar.set)
        # self.update_scrollbar(['a','b','c',('sdsdsd',['as','bs']),'file'])
        self.tree_list.bind('<<ListboxSelect>>',self.update_buttons)
        self.tree_list.pack(side=LEFT, fill=BOTH)
        self.scrollbar.config(command=self.tree_list.yview)

        self.tree_frame.pack()



        self.back_botton=Button(bottom_left_frame,text="<| Back",fg="Black", width=7, height=2,state='disabled')
        self.back_botton.pack( side=BOTTOM  )

        self.enter_botton=Button(bottom_left_frame,text="Enter |>",fg="Black", width=7, height=2,state='disabled')
        self.enter_botton.pack( side=BOTTOM  )

        self.decrypt_botton=Button(bottom_left_frame,text="Decrypt",fg="Black", width=7, height=2, command=self.encrypt,state='disabled')
        self.decrypt_botton.pack( side=BOTTOM  )

        self.encrypt_botton=Button(bottom_left_frame,text="Encrypt",fg="Black", width=7, height=2,command=self.decrypt,state='disabled')
        self.encrypt_botton.pack( side=BOTTOM )

        load_tree_botton=Button(bottom_left_frame,text="Load Tree",fg="black", width=7, height=2,command= self.load_tree)
        load_tree_botton.pack()


        root.mainloop()

    def get_combobox_value(self):
        return self.ips.get()

    def encrypt(self):
        #print "hi"
        #self.decrypt_botton.config(state='disabled')
        self.server.encrypt(self.get_combobox_value(), self.get_path())

    def decrypt(self):
        self.server.decrypt(self.get_combobox_value(), self.get_path())



    def get_path(self):

        path = os.path.join(*self.path)
        return os.path.join(path,self.get_selected_item())

    def update_scrollbar(self, lst):
        self.tree_list.delete(0, self.tree_list.size())
        self.folders=[]
        self.files=[]
        for val in lst:
            if type(val) == tuple:
                self.tree_list.insert(END, val[0])
                self.folders.append(val[0])
            else:
                self.tree_list.insert(END, val)
                self.files.append(val)

    def update_ips(self):
        self.ip_list = self.server.get_ip_list()
        # self.ips.config(values= self.ip_list)
        self.ips['values'] = self.ip_list

    def get_selected_item(self):
        return self.tree_list.get(self.tree_list.curselection())

    def disable_buttons(self,*buttons):
        for button in buttons:
            button.config(state ='disabled')

    def enable_button(self,*buttons):
        for button in buttons:
            button.config(state = 'active')

    def load_tree(self):
        self.disable_buttons(self.back_botton,self.enter_botton,self.enter_botton,self.decrypt_botton)
        ip = self.get_combobox_value()
        soc =  self.server.socket_by_ip(ip)
        tree = self.server.client_dict[soc][1]
        tree = ['yosi.py','baba.txt',('folder',['yosi.asm'])]
        self.update_scrollbar(tree)

    def update_buttons(self,event):
        selected_item = self.get_selected_item()
        #if it is a file
        if selected_item in self.files:
            # disable open and back buttons
            self.enter_botton.config(state = 'disabled')
            self.back_botton.config(state =  'disabled')

            # if it is encrypted disable encryption and enable encryption
            if selected_item in self.server.get_encrypted_files():
                self.encrypt_botton.config(state= 'disabled')
                self.decrypt_botton.config(state = 'active')

            # disable decryption and enable encryption
            else:
                self.encrypt_botton.config(state='active')
                self.decrypt_botton.config(state='disabled')
        # this is a folder
        else:
            self.enter_botton.config(state = 'active')
            self.back_botton.config(state= 'active')
            self.decrypt_botton.config(state= 'disabled')
            self.encrypt_botton.config(state = 'disabled')



g=GUI()