def xor(s, key):
    ciphertext = b''
    for i in range(len(s)):
        ciphertext += bytes([s[i] ^ key[i % len(key)]])
    return ciphertext

def xor_bytes(bytes1: bytes, bytes2: bytes) -> bytes:
    if len(bytes1) != len(bytes2):
        raise ValueError("Byte sequences must be of the same length")
    return bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))

with open("flag.enc", "rb") as f:
    flag = f.read()

header = bytes.fromhex("89504e470d0a1a0a")

key = xor(flag[:8], header)

print(key)

with open('flag.png', 'wb') as f:
    f.write(xor(flag, key))
