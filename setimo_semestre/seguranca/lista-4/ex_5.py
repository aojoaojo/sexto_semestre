def xor(s, key):
    ciphertext = b''
    for i in range(len(s)):
        ciphertext += bytes([s[i] ^ key[i % len(key)]])
    return ciphertext

with open('flag_ex5.enc', 'rb') as f:
    flag = f.read()

header = b"%PDF-1.4"

key = xor(flag[:8], header)

print(key)

with open('flag.pdf', 'wb') as f:
    f.write(xor(flag, key))