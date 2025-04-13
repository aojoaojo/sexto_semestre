#!/usr/bin/python
import os

def xor(s, key):
    ciphertext = b''
    for i in range(len(s)):
        ciphertext += bytes([s[i] ^ key[i % len(key)]])
    return ciphertext

with open('./flag.enc', 'rb') as f:
    content = f.read()

# chaves = 'abcdefghijklmnopqrstuvwxyz0123456789'
# chaves = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

# chaves = [
#     '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~',
#     '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '®', '¯',
#     '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿',
#     'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï',
#     'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß',
#     'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï',
#     'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ'
# ]

with open ('./flags_tested.txt', 'r') as f:
    chaves = f.read().split('\n')

try:
    while True:
        a = os.urandom(1)
        if a in chaves:
            continue
        chaves.append(a)
        print(a)
        possible_picture = xor(content, a)
        with open(f'./flag_{a}.png', 'wb') as f:
            f.write(possible_picture)
        with open('./flags_tested.txt', 'a') as f:
            f.write(f'{a}\n')
except Exception as error:
    print(error)


# # second part:

# import os
# from flask import Flask, send_file

# app = Flask(__name__)

# @app.route('/')
# def serve_image():
#     if os.path.exists(f'/desafio/flag_a.png'):
#         return send_file(f'flag_a.png', mimetype='image/png')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=1337)
