from socket import socket
from select import select
import pickle
from Crypto.PublicKey import RSA
from threading import Thread


class Server(object):
    def __init__(self):
        self.server_soc = socket()
        self.server_soc.bind(('127.0.0.1', 5001))
        self.server_soc.listen(5)
        self.client_dict = {}#  {socket : [ip,tree] }
        self.tree_waiting = {}# {soc: length of the tree in bytes} - represents length's of user's tree before receiving it

    def convert_to_tree(self, string):
        return pickle.loads(string)

    def ip_by_socket(self,soc):
        return self.client_dict[soc][0]

    def socket_by_ip(self,ip):
        for soc in self.client_dict:
            if self.client_dict[soc][0] == ip:
                return soc

    def manage_clients(self):
        client_list = self.client_dict.keys()
        rlst, _, _ = select([self.server_soc]+client_list, [], [],0)
        for soc in rlst:
            # if there is a new client waiting to connect
            # the tree for every new client initialized as empty list
            # sends request for tree
            if soc is self.server_soc:
                client_soc, address = soc.accept()
                print address[0], "logged in"
                self.client_dict[client_soc] = [address[0], []]
                client_soc.send('len')

            # the client sent a tree
            elif soc in self.tree_waiting.keys():
                print "len" , self.tree_waiting[soc]
                length=0
                data = ''
                while length < self.tree_waiting[soc]:
                    data += soc.recv(self.tree_waiting[soc])
                    length += len(data.encode('utf-8'))
                    print length
                # data = soc.recv(2**25)
                #print len(data.encode('utf-8'))
                self.client_dict[soc][1] = self.convert_to_tree(data)
                del self.tree_waiting[soc]
                print self.ip_by_socket(soc), 'sent a tree'

            # the client sent the tree's length
            else:
                length = int(soc.recv(1024))
                print length
                self.tree_waiting[soc] = length
                soc.send('dirs')
                print self.ip_by_socket(soc), 'sent length'
            # if the socket is waiting for a tree to be sent - receive the tree
            # remove from tree_waiting
            """
            elif soc in self.tree_waiting.keys():
                tree = self.convert_to_tree(soc.recv(self.tree_waiting[soc]))
                self.client_dict[soc][1] = tree
                del self.tree_waiting[soc]
                print self.ip_by_socket(soc), 'sent a tree'

            else:
                tree_len = int(soc.recv(1024))
                self.tree_waiting[soc] = tree_len
                print self.ip_by_socket(soc), 'preparing to send a tree'
"""
            #elif soc in expectation:
                #recv(len_expec)

            #else:
                #  expectation.append((soc, a)) #a is length

    # add file name to the keys file
    # {ip: {file_name: key}}
    def add_key(self,ip,key,file_name):
        try:
            read_file = open('keys.eio', 'rb')
            ips = pickle.load(read_file)
            if ip not in ips.keys():
                ips[ip] = {}
            ips[ip][file_name] = key
            read_file.close()

            write_file = open('keys.eio', 'wb')
            pickle.dump(ips, write_file)
            read_file.close()
            write_file.close()

        # if the file dosen't exist
        except IOError:
            write_file = open('keys.eio', 'wb')
            ips = {}
            ips[ip] = {}
            ips[ip][file_name] = key
            pickle.dump(ips, write_file)
            write_file.close()

    def encrypt(self, ip, file_name):
        # generate key
        key = RSA.generate(2048)
        # save the key in a file
        self.add_key(ip, key, file_name)
        # send the command
        self.socket_by_ip(ip).send('encrypt ' + file_name + ' '+ key.publickey().exportKey())

    def find_key(self, ip, file_name):
        read_file = open('keys.eio', 'rb')
        ips = pickle.load(read_file)
        key = ips[ip][file_name]
        del ips[ip][file_name]
        read_file.close()

        write_file = open('keys.eio', 'wb')
        pickle.dump(ips, write_file)
        write_file.close()

        return key



    def decrypt(self, ip, file_name):
        # find the key and delete
        key = self.find_key(ip, file_name)
        print 'key', key.exportKey()
        # send the key
        self.socket_by_ip(ip).send('decrypt ' + file_name + ' ' + key.exportKey())

    def run(self):
        self.test = 'a'
        while 'Encrypt.io':
            self.manage_clients()
            # test
            if self.test == 'e':
                self.encrypt('127.0.0.1',r'C:\Users\barhen\Desktop\normal.txt')
            elif self.test == 'd':
                self.decrypt('127.0.0.1',r'C:\Users\barhen\Desktop\normal.txt')


    def run_thread(self):
        t = Thread(target=self.run)
        t.start()



# s = Server()
# s.run()




