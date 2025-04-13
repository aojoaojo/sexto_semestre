from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key_hex = "7a8abf2ab084f6e9544a0304576a1c98"
frase = "AAAAAAAAAAAAAAAA"

key = bytes.fromhex(key_hex)
padded = pad(frase.encode(), 16)
cipher = AES.new(key, AES.MODE_ECB)
ct = cipher.encrypt(padded)
print(ct.hex())