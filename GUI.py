from tkinter import *
import server

class GUI(object):
    def __init__(self):
        self.root = Tk()
        self.server = server.Server()
        self.server.run_thread()

        self.enteries = Frame(self.root)
        self.ip = Entry(self.enteries)
        self.file = Entry(self.enteries)

        self.buttons = Frame(self.root)

        enc_fun = lambda: self.server.encrypt(self.ip.get(), self.file.get())
        dec_fun = lambda: self.server.decrypt(self.ip.get(), self.file.get())
        self.encrypt_button = Button(self.buttons, text='encrypt', command=enc_fun)
        self.decrypt_button = Button(self.buttons, text='decrypt', command=dec_fun)

        self.enteries.pack()
        self.buttons.pack(side=BOTTOM)

        self.ip.pack(side=LEFT)
        self.file.pack(side=RIGHT)

        self.encrypt_button.pack(side=LEFT)
        self.decrypt_button.pack(side=RIGHT)

        self.root.mainloop()


g = GUI()
