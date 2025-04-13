import socket
import time
import random

server = '74.235.160.126'
port = 33118

def conectar():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    return s

def encontrar_seed(primeiro_numero):
    tempo_atual = int(time.time())
    
    for seed in range(tempo_atual - 30, tempo_atual + 2):  # Testamos um pequeno intervalo de tempo
        random.seed(seed)
        if random.getrandbits(32) == primeiro_numero:
            return seed
    
    return None

def resolver_desafio(s):
    s.send(b'2\n')
    
    print(s.recv(1024).decode())
    print(s.recv(1024).decode())
    
    s.send(b'1\n')

    dados = s.recv(1024).decode()
    print(dados)

    for linha in dados.split("\n"):
        if "eu estava pensando no número:" in linha:
            primeiro_numero = int(linha.split(":")[-1].strip())
            break

    print(f"[+] Primeiro número do desafio: {primeiro_numero}")

    seed = encontrar_seed(primeiro_numero)
    
    if seed is None:
        print("[-] Não foi possível determinar o seed.")
        return
    
    print(f"[+] Seed encontrado: {seed}")

    random.seed(seed)

    numero_correto = random.getrandbits(32)
    for i in range(25):  
        numero_correto = random.getrandbits(32)
        print(f"[+] Tentando número: {numero_correto}")
        s.send(f"{numero_correto}\n".encode())
        resposta = s.recv(1024).decode()
        print(resposta)

        if "Flag" in resposta:
            print("[+] FLAG ENCONTRADA!")
            break

def main():
    s = conectar()
    
    resolver_desafio(s)

    s.close()

main()
