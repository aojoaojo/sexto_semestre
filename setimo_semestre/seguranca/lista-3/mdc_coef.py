import socket
from sympy import gcdex

# Configuração do servidor
host = '74.235.160.126'
porta = 33454

# Conectar ao servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, porta))

    while True:
        
        dados = s.recv(1024).decode('utf-8')
        
        print("passou 1")

        if "Flag" in dados:
            print(dados)
            break

        print("passou 2")

        dados = dados.split()
        num1 = int(dados[-6])
        num2 = int(dados[-5])
        
        print("passou 3")
        
        print(f"Números recebidos: {num1}, {num2}")
        
        a, b = num1, num2
        print("passou 4")

        # Calcular o GCD e os valores de m e n usando a função gcdex da sympy
        gcd, m, n = gcdex(a, b)
        print("passou 5")

        # Montar a resposta no formato correto
        resposta = f"{gcd} {m} {n}"
        print("passou 6")
        
        # Enviar o resultado ao servidor
        s.sendall(str(f'{resposta}\n').encode('utf-8'))
        print(f"Resultado enviado: {resposta}")
        print("passou 7")

