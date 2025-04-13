
import os
import random
import string
import base64

def xor(s, key):
    return b''.join([bytes([ord(c) ^ key]) for c in s])

flag = 'IDP-CS{TESTE}' if not os.access('flag.txt', os.R_OK) else open('flag.txt').read().strip()

# c = random.choice(string.ascii_letters)

flag1 = 'BQgcYQ8fNy5+dHp/eip6Knh0dX8oeioqKn0pe3V+eS55enQudHV7MQ=='

c = 'L'
print(f'Char   : {c}')
print(f'Desafio: {base64.b64encode(xor(flag, ord(c)))}')

# Char   : L
# Desafio: BQgcYQ8fNy5+dHp/eip6Knh0dX8oeioqKn0pe3V+eS55enQudHV7MQ==

