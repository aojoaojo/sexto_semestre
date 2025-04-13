from pwn import *
import time
import random
import os
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import DES

def pad(s):
    return s.encode() + b'*' * (8 - len(s) % 8)


text_enc = "6241cc694c94e108f4cb294a9951818b40680d4cd8c0f7039c024b0e55adedfff8bef5e87a30cd36ade2b178cdc9341f"

lista= [
    "0101010101010101",
    "FEFEFEFEFEFEFEFE",
    "E0E0E0E0F1F1F1F1",
    "1F1F1F1F0E0E0E0E",
]

key = lista[3]
cipher = DES.new((bytes.fromhex(key)), DES.MODE_ECB)

decoded_text = bytes.fromhex(text_enc)
decrypted_text = cipher.decrypt(decoded_text)
print(decrypted_text)

# try:
#     result = unpad(decrypted_text, 8).decode()
#     print("Decrypted text:", result)
# except ValueError:
#     print("Failed to decrypt or unpad the text.")