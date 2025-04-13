from pwn import *

host = '74.235.160.126'
port = 33173

META =  1337

def take_response_and_print(conn, op=1):

    resposta = conn.recv().decode()

    if op != 1:
        money = resposta.split(':')[1].strip().split('<')[0].strip()
        print('money', money)
        print(resposta)
        return int(money)

    print(resposta)

def apostar(conn, money):
    conn.send(b'1\n')
    print('1:')
    take_response_and_print(conn)

    conn.send(b'3\n') #aposta

    print('2:')
    money = take_response_and_print(conn, money)

    return money

def start(conn):
    money = 0

    conn.recvline()

    take_response_and_print(conn)

    conn.send(b'2\n')

    take_response_and_print(conn)

    while True:
        if money > META:
            conn.send(b'2\n')
            take_response_and_print(conn)
            return money
        money = apostar(conn, money)

while True:
    try:
        conn = remote(host, port)
        money = start(conn)
        if money > META:
            take_response_and_print(conn)
            i = input('opt: ')
            conn.send(i.encode() + b'\n')
            break
    except EOFError:
        print("EOFError")
        conn.close()
        continue
    except Exception as e:
        print(f"Exception: {e}")
        conn.close()
        continue