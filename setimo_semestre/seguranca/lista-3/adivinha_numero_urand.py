import socket
from randcrack import RandCrack

def capture_numbers(host, port, count=624):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    captured_numbers = []

    s.send(b'2\n')
    
    print(s.recv(1024).decode())
    print(s.recv(1024).decode())

    while len(captured_numbers) < count:
        s.send(b"1\n")
        data = s.recv(1024).decode()
        for linha in data.split("\n"):
            if "eu estava pensando no número:" in linha:
                captured = int(linha.split(":")[-1].strip())
                captured_numbers.append(int(captured))
        print('tamanho:', len(captured_numbers))
        print('[-] sent 1')
        print(data)

    print('finish 1')
    
    p = predict_next(captured_numbers)
    captured_numbers.append(int(p))

    print('finish 2')

    for a in range(25):
        print(f'{a} - {len(captured_numbers)}')
        p = predict_next(captured_numbers)
        s.send(f"{p}\n".encode())
        print(f"[+] Predicted: {p}")
        data = s.recv(1024).decode()
        print(data)
        if "Flag" in data:
            print("Flag found!")
            break

    s.close()
    return captured_numbers

def predict_next(captured_numbers):
    rc = RandCrack()
    for number in captured_numbers:
        rc.submit(number)
    return rc.predict_getrandbits(32)

if __name__ == "__main__":
    host = "74.235.160.126"
    port = 33366
    
    print("Capturing numbers...")
    numbers = capture_numbers(host, port)