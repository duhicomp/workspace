'''
Created on Jan 18, 2015

@author: Duhi
'''

import hashlib
import os
def calc_hash(in_file_path):
    
    file_to_hash_path = in_file_path
    print("Calculating the filesize of: " + file_to_hash_path)
    with open(file_to_hash_path, 'rb') as f:
        sha1 = hashlib.sha224()
        while True:
            data =  f.read(4096 * 10)
            if not data:
                break
            sha1.update(data)
    print("File Path:" + file_to_hash_path + "File size:" + 
          str(os.path.getsize(file_to_hash_path) ) + " Hash:" +str(sha1.hexdigest()))
    
        
if __name__ =="__main__":
    in_file_path="D:\\NAS\\CentOS-7.0-1406-x86_64-DVD\\CentOS-7.0-1406-x86_64-DVD.iso"
    calc_hash(in_file_path)
