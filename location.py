import win32api
import win32con

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
    if is_system_file(file_name) or is_device_file(file_name)\
    or is_readonly_file(file_name) or is_temp_file(file_name)\
    or is_virtual_file(file_name):
        return False
    return True

def get_dirs():
    drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
    




print is_system_file(r'C:\Users\student\Desktop\New Text Document.txt')
print is_device_file(r'C:\Users\student\Desktop\New Text Document.txt')
print is_directory(r'C:\Users\student\Desktop')
print is_readonly_file(r'C:\Users\student\Desktop\New Text Document.txt')
print is_suitable_file(r'C:\Users\student\Desktop\New Text Document.txt')


