#!/usr/bin/python

import os
from base64 import b64encode, b64decode

def xor(s, key):
    ciphertext = b''
    for i in range(len(s)):
        ciphertext += bytes([s[i] ^ key[i % len(key)]])
    return ciphertext

ciphertext = 'OR5vE9h+GL4WPl0KohRRvhE+CQupHVe5EzkIDKNMUulJbwdbrhoHpQ=='
ciphertext = b64decode(ciphertext)

layout = 'IDP-CS{'

nexts = 'abcdefghijklmnopqrstuvwxyz0123456789'

for c in nexts:
    key = xor(ciphertext, (layout + c).encode())
    key = key[:8]
    a = xor(ciphertext, key)
    print(a)

