import os
from collections import Counter

# Função para aplicar XOR em uma sequência de bytes com uma chave
def xor_bytes(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

# Função para analisar a frequência dos bytes no arquivo cifrado
def analisar_frequencia(dados_cifrados):
    contador = Counter(dados_cifrados)
    print("Frequência dos bytes no arquivo cifrado:")
    for byte, freq in contador.most_common(10):
        print(f"Byte: {byte:02X} - Frequência: {freq}")

# Função para tentar descriptografar o arquivo cifrado
def tentar_descriptografar(arquivo_cifrado):
    # Ler os dados do arquivo cifrado
    with open(arquivo_cifrado, "rb") as f:
        dados_cifrados = f.read()
    
    # Analisar frequência dos bytes cifrados
    analisar_frequencia(dados_cifrados)
    
    # Tentativas com padrões conhecidos (por exemplo, cabeçalho de um arquivo PNG)
    cabecalho_png = b'\x89PNG\r\n\x1a\n'
    
    # Tentar chaves de 1 a 8 bytes
    for chave_tamanho in range(1, 9):
        for i in range(256 ** chave_tamanho):
            chave = i.to_bytes(chave_tamanho, 'big')
            dados_decifrados = xor_bytes(dados_cifrados, chave)
            
            if dados_decifrados.startswith(cabecalho_png):
                print(f"Arquivo possivelmente restaurado com chave: {chave}")
                
                with open("flag.png", "wb") as f:
                    f.write(dados_decifrados)
                
                print("Arquivo salvo como flag.png")
                return
    
    print("Não foi possível restaurar o arquivo com chaves de até 8 bytes.")

# Caminho do arquivo cifrado
arquivo_cifrado = "flag.enc"

if os.path.exists(arquivo_cifrado):
    tentar_descriptografar(arquivo_cifrado)
else:
    print("Arquivo flag.enc não encontrado.")
