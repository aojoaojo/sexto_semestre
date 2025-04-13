import socket
import math

# Função para calcular o MDC
def calcular_mdc(a, b):
    return math.gcd(a, b)

# Configuração do servidor
host = '74.235.160.126'
porta = 33452

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, porta))

    # Receber a frase do servidor (com um tamanho máximo arbitrário de 1024 bytes)
    while True:

        frase = s.recv(1024).decode('utf-8')

        print(f"Frase recebida: {frase}")

        if "Flag" in frase:
            print(frase)
            break
        print('passou 1')
        palavras = frase.split()
        print('passou 2')
        num1 = int(palavras[-4])  # Penúltima palavra
        print('passou 3')
        num2 = int(palavras[-3])  # Última palavra
        print('passou 4')

        # Calcular o MDC
        mdc = calcular_mdc(num1, num2)
        print('passou 5')

        # Enviar o resultado de volta para o servidor
        s.sendall(str(f'{mdc}\n').encode('utf-8'))

        print('passou 6')

        print(f"Resultado do MDC enviado: {mdc}")