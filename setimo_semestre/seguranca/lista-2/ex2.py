#!/usr/bin/python

import os
from base64 import b64encode, b64decode

def xor(s, key):
    ciphertext = b''
    for i in range(len(s)):
        ciphertext += bytes([s[i] ^ key[i % len(key)]])
    return ciphertext

layout = 'IDP-CS{'

ciphertext = '2w0czrsJfqtxetvAaWehLH3Qz2syoXkp0sFiMKYtLdTPbmH2en7VhQ=='
ciphertext2 = b64decode(ciphertext)


key = xor(ciphertext2, layout.encode())
key = key[:7]
print(len(key))
a = xor(ciphertext2, key)

print(a)
