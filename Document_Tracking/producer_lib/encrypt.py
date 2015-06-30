#!/usr/bin/env python

import os
import base64
import sys
from Crypto.Cipher import DES

def encrypt(a):

   obj=DES.new("\x7F\xDB\x3E\xDB\xFB\xFA\x1A\x19", DES.MODE_ECB)
   
   if len(a) > 16:
     raise Exception("password too long")   
     
   padded = a.ljust(16)

   return base64.encodestring(obj.encrypt(padded))  
   
def decrypt(a):

   obj=DES.new("\x7F\xDB\x3E\xDB\xFB\xFA\x1A\x19", DES.MODE_ECB)
   
   padded = obj.decrypt(base64.decodestring(a))

   return padded.strip().strip("\b")
   
if __name__ == "__main__":
      
     encrypted = encrypt(sys.argv[1])
       
     print "encrypted value for " + sys.argv[1] + " is "  + encrypted
        