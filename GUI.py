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

        self.ips=ttk.Combobox(up_frame, values= self.ip_list, postcommand=self.update_ips , width=80, state='readonly')
        self.ips.pack()
        # Thread(target=self.update_ips).start()

        self.path = []

        self.scrollbar = Scrollbar(self.tree_frame)
        self.scrollbar.pack(side=LEFT, fill=Y)

        self.tree_list = Listbox(self.tree_frame, yscrollcommand=self.scrollbar.set)
        # self.update_scrollbar(['a','b','c',('sdsdsd',['as','bs']),'file'])

        self.tree_list.pack(side=LEFT, fill=BOTH)
        self.scrollbar.config(command=self.tree_list.yview)

        self.tree_frame.pack()



        back_botton=Button(bottom_left_frame,text="<| Back",fg="Black", width=7, height=2,state='disabled')
        back_botton.pack( side=BOTTOM  )

        enter_botton=Button(bottom_left_frame,text="Enter |>",fg="Black", width=7, height=2,state='disabled')
        enter_botton.pack( side=BOTTOM  )

        self.decrypt_botton=Button(bottom_left_frame,text="Decrypt",fg="Black", width=7, height=2, command=self.encrypt,state='disabled')
        self.decrypt_botton.pack( side=BOTTOM  )

        encrypt_botton=Button(bottom_left_frame,text="Encrypt",fg="Black", width=7, height=2,command=self.decrypt,state='disabled')
        encrypt_botton.pack( side=BOTTOM )

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
        for val in lst:
            if type(val) == tuple:
                self.tree_list.insert(END, val[0])
                self.folders.append(val[0])
            else:
                self.tree_list.insert(END, val)
                self.folders.append(val)

    def update_ips(self):
        self.ip_list = self.server.get_ip_list()
        # self.ips.config(values= self.ip_list)
        self.ips['values'] = self.ip_list

    def get_selected_item(self):
        return self.tree_list.get(self.tree_list.curselection())

    def load_tree(self):
        ip = self.get_combobox_value()
        soc =  self.server.socket_by_ip(ip)
        tree = self.server.client_dict[soc][1]
        self.update_scrollbar(tree)




g=GUI()