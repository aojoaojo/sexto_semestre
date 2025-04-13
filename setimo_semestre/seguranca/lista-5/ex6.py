from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key_hex = "64fa01eb775ffdeb595af96d7ba7af34"
ciphertext_hex = "add0ac4f2cf09ca2e582986908cdb7029e9ebc13821e404b61c0edb551375f4c171d305e31861c7619c40ce66457d12c"

key = bytes.fromhex(key_hex)
ciphertext = bytes.fromhex(ciphertext_hex)

cipher = AES.new(key, AES.MODE_ECB)
decrypted = cipher.decrypt(ciphertext)

try:
    plaintext = unpad(decrypted, 16).decode()
    print("[FLAG]", plaintext)
except ValueError:
    print("Erro no unpad. Texto descriptografado:", decrypted)
