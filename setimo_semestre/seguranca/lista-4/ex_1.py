from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

key = bytes.fromhex('4fd04a528c14f897')
m_encrypted = bytes.fromhex('1832b038c9413560a750313cbd04503cae5c6d7caaa01a1cedba0bb80d593758ad88f9ce8d559ddb')

cipher = DES.new(key, DES.MODE_ECB)

print(cipher.decrypt(m_encrypted).decode())