from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from pwn import remote
from Crypto.Cipher import AES

SERVER = '74.235.160.126'
PORT = 32815

def connect_to_server():
    io = remote(SERVER, PORT)
    return io

def get_encrypted_message(io):
    msg = io.recvall(timeout=3).decode()
    print(msg)

def get_key(io):
    io.recvuntil(b"Chave: ")
    key = io.recvline().strip()
    return key

def decrypt_message(key, encrypted_message):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message

def extract_info_1(response):
    response = response.splitlines()
    key = response[1].split(': ')[1]
    msg = response[2].split(': ')[1:][0]
    return bytes.fromhex(key), msg

def extract_info_2(response):
    msg = response.decode()
    msg = msg.split(': ')[1:][0]
    return msg

def main():
    io = connect_to_server()
    response = io.recv(timeout=3).decode()
    key, msg = extract_info_1(response)

    while True:
        padded_msg = pad(msg.encode(), 16)
        cipher = AES.new(key, AES.MODE_ECB)
        ct = cipher.encrypt(padded_msg)
        io.sendline(ct.hex().encode())
        response = io.recv(timeout=3)
        if b"flag" in response:
            print("Resposta correta!")
            print(response.decode())
            break
        msg = extract_info_2(response)
        print(msg)

main()