import os
from base64 import b64decode

def xor(s, key):
    ciphertext = b''
    for i in range(len(s)):
        ciphertext += bytes([s[i] ^ key[i % len(key)]])
    return ciphertext

quote = "Meu plano é ser rico e misterioso. Parece que só acertei no misterioso."

ciphertext1 = 'KimQO5Ae+yE4j5b4lR+DxDF+wXo1eFdaik5+RjQV+yHjunmmre009A=='
ciphertext2 = 'Lgi1NqMh4X4zmm1phl+Dh3Q8yy9pYQRKgx47AWQBoCuj5DSxyO9+7AA='

ciphertext1 = b64decode(ciphertext1)
ciphertext2 = b64decode(ciphertext2)

key = xor(ciphertext2, quote.encode())

resposta_braba = xor(key, ciphertext1)

print(resposta_braba)