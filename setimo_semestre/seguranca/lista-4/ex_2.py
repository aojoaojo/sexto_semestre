from pwn import *
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import DES


# host = '3.88.51.10'
host = '74.235.160.126'
port = 33028

conn = remote(host, port)
conn.recvline()

def pega_info_chave(string):
    key = string.split(":")[1].split("\n")[0].strip()
    msg = string.split(":", 2)[2].split("\n")[0].strip()
    return key, msg

def pega_info(string):
    msg = string.split("Desafio (")[1].split("):")[1].split("\n")[0].strip()
    return msg

resposta = ''
flag = 0
while True:  
    
    resposta = conn.recv().decode()
    print(resposta)
    if('IDP' in resposta):
        print(resposta)
        break
    if flag == 0:
        key, msg = pega_info_chave(resposta)
        cipher = DES.new((bytes.fromhex(key)), DES.MODE_ECB)
        flag = 1
    else:
        msg = pega_info(resposta)
    # print(key)
    print(msg)
    msg_bytes = msg.encode()
    
    if len(msg_bytes) == 8:
        msg_bytes += b'\0' * 8
        
    elif len(msg_bytes) % 8 != 0:
        msg_bytes += b'\0' * (8 - len(msg_bytes) % 8)

    msg_enc = cipher.encrypt(msg_bytes)
    print(msg_enc.hex())
    conn.send((msg_enc.hex() + '\n').encode())
    # print(conn.recv().decode())