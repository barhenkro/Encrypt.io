import win32api
import win32con
import os

def is_attrib_file(file_name, attrib):
    
    file_attrib = win32api.GetFileAttributes(file_name) 
    return attrib & file_attrib == attrib

def is_system_file(file_name):
    return is_attrib_file(file_name,win32con.FILE_ATTRIBUTE_SYSTEM)

def is_device_file(file_name):
    return is_attrib_file(file_name, win32con.FILE_ATTRIBUTE_DEVICE)

def is_readonly_file(file_name):
        return is_attrib_file(file_name, win32con.FILE_ATTRIBUTE_READONLY)

def is_temp_file(file_name):
        return is_attrib_file(file_name, win32con.FILE_ATTRIBUTE_TEMPORARY)

def is_virtual_file(file_name):
        return is_attrib_file(file_name, win32con.FILE_ATTRIBUTE_VIRTUAL)
    
def is_directory(dir_name):
    return is_attrib_file(dir_name, win32con.FILE_ATTRIBUTE_DIRECTORY)

def is_suitable_file(file_name):
    try:
        if is_system_file(file_name) or is_device_file(file_name)\
        or is_readonly_file(file_name) or is_temp_file(file_name)\
        or is_virtual_file(file_name):
            return False
        return True
    except:
        return False

def get_disks():
    drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]

def get_tree(path):
    tree=[]
    root, dirs, files=next(os.walk(path))
    for f in files:
        print (os.path.join(path,f))
        if is_suitable_file(os.path.join(path,f)):
            tree.append(f)
    for d in dirs:
        print (os.path.join(path,d))
        if is_suitable_file(os.path.join(path,d)):
            try:
                tree.append((d, get_tree(os.path.join(root,d))))
            except StopIteration:
               pass 
    return tree
    
    
    
    




#print is_system_file(r'C:\Users\shaked\Desktop\hi')
#print is_device_file(r'C:\Users\shaked\Desktop\hi')
#print is_directory(r'C:\Users\shaked\Desktop')
#print is_readonly_file(r'C:\Users\shaked\Desktop\hi')
#print is_suitable_file(r'C:\Users\shaked\Desktop\hi')
a=get_tree('C:\\')
#next(os.walk(r'C:\ProgramData\Avg\Antivirus\SecureLine'))



