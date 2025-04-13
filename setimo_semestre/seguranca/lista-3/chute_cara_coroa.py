import socket
import random

server = '74.235.160.126'
port = 33114

def conectar():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((server, port))

    s.recv(1024)

    s.send(b'2\n')

    return s

def chute(s):
    for _ in range(5):
        number = random.randint(1, 2)

        if number == 1:
            s.send(b'cara\n')
        else:
            s.send(b'coroa\n')

        resposta = s.recv(1024).decode()
        print(resposta)

        if (resposta == 'Errado!\n'):
            s.close()
            return False
    print(s.recv(1024).decode())
    return True
        
def main():
    while True:
        s = conectar()
        k = chute(s)
        if k:
            break
main()