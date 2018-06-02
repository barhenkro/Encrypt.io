from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

# gets exported key and file's name
# encrypts the file with the key
def encrypt(exported_key,file_name):
    new_text = ''
    public_key = RSA.importKey(exported_key)
    chunk = (public_key.size()+1)/8-11
    cipher = PKCS1_v1_5.new(public_key)
    with open(file_name, 'rb') as f:
        data = f.read(chunk)
        # print public_key.size()
        while data!='':
            new_text =  new_text + cipher.encrypt(data) 
            data = f.read(chunk)

    with open(file_name,'wb')as f:
        f.write(new_text)
    print new_text

# gets exported key and file's name
# key must be private
# decrypts the file with the key
def decrypt(exported_key,file_name):
    new_text = ''
    private_key = RSA.importKey(exported_key)
    chunk = (private_key.size()+1)/8
    cipher = PKCS1_v1_5.new(private_key)
    with open(file_name, 'rb') as f:
        data = f.read(chunk)
        print data
        # print public_key.size()
        while data!='':
            new_text =  new_text + cipher.decrypt(data,2) 
            data = f.read(chunk)

    with open(file_name,'wb')as f:
        f.write(new_text)





            

# # encrypt(RSA.generate(1024).publickey().exportKey(),'aaa.txt')
# my_key = RSA.generate(2048)
# print my_key.exportKey()
# encrypt(my_key.publickey().exportKey(),'45601.jpg')
# decrypt(my_key.exportKey(),'45601.jpg')

        
        
    
    
    
