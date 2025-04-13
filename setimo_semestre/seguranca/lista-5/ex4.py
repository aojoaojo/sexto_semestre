from pwn import *

context.log_level = 'error'
HOST = '74.235.160.126'
PORT = 32788

xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_single_column(a):
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)

def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])

def inv_mix_columns(s):
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v
    mix_columns(s)

def inv_shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]

def matrix2bytes(matrix):
    return b''.join(bytes(row) for row in matrix)

def extrair_matriz(bloco):
    matriz = []
    for linha in bloco.strip().splitlines():
        if '[' in linha and ']' in linha:
            linha = linha.replace('[', '').replace(']', '').strip()
            matriz.append(list(map(int, linha.split(','))))
    return matriz

def main():
    r = remote(HOST, PORT)
    r.recvuntil("Opção:".encode())
    r.sendline(b"2")

    for i in range(5):
        output = r.recvuntil("Resposta:".encode()).decode()
        bloco_s = output.split("S2 = [")[1].split("     ]")[0] + "]"
        S = extrair_matriz(bloco_s)
        inv_mix_columns(S)
        inv_shift_rows(S)
        resposta = matrix2bytes(S)
        print(f"[{i+1}/5] Enviando: {repr(resposta)}")
        r.sendline(resposta)

    final = r.recvall(timeout=2).decode()
    print("\n" + final.strip())

if __name__ == "__main__":
    main()
