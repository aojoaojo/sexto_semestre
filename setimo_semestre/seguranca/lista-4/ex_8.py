from Crypto.Cipher import DES
import itertools
import os
from string import digits

BLOCK_LEN = 8

def padding(S):
    return S + ' ' * (BLOCK_LEN - (len(S) % BLOCK_LEN))

def DDES_encrypt(m, k1, k2):
    cp1 = DES.new(k1, DES.MODE_ECB)
    cp2 = DES.new(k2, DES.MODE_ECB)
    return cp2.encrypt(cp1.encrypt(padding(m).encode()))

def DDES_decrypt(c, k1, k2):
    cp1 = DES.new(k1, DES.MODE_ECB)
    cp2 = DES.new(k2, DES.MODE_ECB)
    return cp1.decrypt(cp2.decrypt(c)).strip()

# Exemplo: ataque meet-in-the-middle
def generate_keys(prefix):
    # Gera todas as combinações de 7 dígitos para completar uma chave de 8 dígitos
    for key_suffix in itertools.product(digits, repeat=7):
        yield (prefix + ''.join(key_suffix)).encode()

def attack(known_plaintext, known_ciphertext, key1_prefix, key2_prefix):
    intermediate = {}
    # Fase 1: para cada chave K1 com o prefixo dado, ciframos o known_plaintext
    for k1 in generate_keys(key1_prefix):
        cp1 = DES.new(k1, DES.MODE_ECB)
        inter = cp1.encrypt(padding(known_plaintext).encode())
        intermediate[inter] = k1

    print(f"[DEBUG] Total de valores intermediários gerados: {len(intermediate)}")

    # Fase 2: para cada chave K2 com o prefixo dado, deciframos o known_ciphertext
    for k2 in generate_keys(key2_prefix):
        cp2 = DES.new(k2, DES.MODE_ECB)
        inter_dec = cp2.decrypt(known_ciphertext)
        if inter_dec in intermediate:
            k1 = intermediate[inter_dec]
            print(f"[DEBUG] Chaves encontradas: K1 = {k1.decode()}, K2 = {k2.decode()}")
            return k1, k2
    return None, None

# Dados do desafio
# Texto conhecido e sua cifra (por exemplo, usando "AAAAAAAA")
known_plaintext = "AAA"
known_ciphertext_hex = "6158d3dbe04c8999"
known_ciphertext = bytes.fromhex(known_ciphertext_hex)

# Dicas dos primeiros dígitos (do desafio: Chave 01: 3, Chave 02: 9)
key1_prefix = "3"
key2_prefix = "8"

k1, k2 = attack(known_plaintext, known_ciphertext, key1_prefix, key2_prefix)
if k1 and k2:
    # Flag cifrada fornecida
    flag_cipher_hex = "da5a60c6f14b810fe43106e819bc0667826d8587279866aa843d7c2d468b8c460c05e1dc5f7053f1b3d18106c4e3fcdf"
    flag_cipher = bytes.fromhex(flag_cipher_hex)
    flag = DDES_decrypt(flag_cipher, k1, k2)
    print(f"Flag descriptografada: {flag.decode()}")
else:
    print("Chaves não encontradas.")
