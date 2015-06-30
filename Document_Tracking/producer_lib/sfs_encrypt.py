#!/usr/bin/env python

#Sefas Crypto

import base64
from Crypto.Cipher import AES


def encrypt(keystore, password):

    fd = open(keystore, 'r')
    key = fd.read()[-16:]
    
    aes = AES.new(key, AES.MODE_CBC)
    
    padded = password.ljust(16, '\b')
    
    return base64.encodestring(aes.encrypt(padded))
    
def decrypt(keystore, password):

    fd = open(keystore, 'r')
    key = fd.read()[-16:]
    
    aes = AES.new(key, AES.MODE_CBC)
    
    return aes.decrypt(base64.decodestring(password)).rstrip("\b")
    
if __name__ == "__main__":

    clear_password = "sefas123"
    encrypted_password = "u6RnzcwrckVxMNBZN8Hj2w=="
    
    keystore = "/adf/openprint/producer/tomcat/webapps/producer/home/httpbeancrypt128"
    
    print "encrypt", "sefas123"
    print encrypt(keystore, clear_password)

    print "decrypt", "u6RnzcwrckVxMNBZN8Hj2w=="
    print decrypt(keystore, encrypted_password)
    
    
    
