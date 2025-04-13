from pwn import *
import time
import random
import os
from math import gcd
from sympy import gcdex

host = '74.235.160.126'
port = 33142

conn = remote(host, port)
conn.recvline()

resposta = conn.recv().decode()
print(resposta)
# resposta = ''

while not("IDP" in resposta):
    parts = resposta.split(':')
    
    if len(parts) > 1:
        numbers = parts[1].strip().split()
        if len(numbers) >= 2:
            num1, num2 = numbers[:2]
    print(num1, num2)
    print(resposta)
    # number = gcdex(int(num1), int(num2))
    # n1, n2, n3 = number
    # send = (str(n1) + ' ' + str(n2) + ' ' + str(n3) + '\n').encode()
    number = int(num1) % int(num2)
    send = str(number) + '\n'   
    # print(send)
    conn.send(send)
    resposta = conn.recv().decode()


print(f"\n\n\n\n\n\n\n\n{resposta}")
print(conn.recv().decode())
   