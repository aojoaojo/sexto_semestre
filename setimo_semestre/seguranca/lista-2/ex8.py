from pwn import *

# Configuração do alvo
host = "74.235.160.126"
port = 33884

# Conectar ao servidor
conn = remote(host, port)

# Receber dados iniciais (se houver)
response = conn.recv()
print(response.decode())

# Enviar um teste (modifique conforme necessário)
conn.sendline(b"Hello, server!")

# Receber resposta
response = conn.recv()
print(response.decode())

# Fechar conexão
conn.close()
