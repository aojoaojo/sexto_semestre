import socket

class CalculatorServer:
    HOST = "127.0.0.1"
    PORT = 12346

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _process_request(self, client_socket, client_address, data):
        print(f"[DADOS] Recebidos de {client_address}: {data}")

        parts = data.strip().split(";")
        if len(parts) != 3:
            client_socket.sendall("[ERRO] Formato da mensagem inválido. Use: OPERACAO;NUM1;NUM2".encode("utf-8"))
            return

        operation = parts[0].upper()
        num1_str, num2_str = parts[1], parts[2]

        try:
            number1 = float(num1_str)
            number2 = float(num2_str)
            
            result = None
            if operation == "SOMA":
                result = number1 + number2
            elif operation == "SUBTRACAO":
                result = number1 - number2
            elif operation == "MULTIPLICACAO":
                result = number1 * number2
            elif operation == "DIVISAO":
                if number2 == 0:
                    result = "[ERRO] Divisão por zero não é permitida."
                else:
                    result = number1 / number2
            else:
                result = f"[ERRO] Operação '{operation}' desconhecida."
            
            response = str(result)

        except ValueError:
            response = "[ERRO] Os números enviados não são válidos."
        
        print(f"[RESPOSTA] Enviando para {client_address}: {response}")
        client_socket.sendall(response.encode("utf-8"))

    def start(self):
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        print(f"[SERVIDOR] Calculadora remota iniciada na porta {self.PORT}. Aguardando conexões...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"[CONEXÃO] Nova conexão estabelecida com {client_address}")

            with client_socket:
                try:
                    data = client_socket.recv(1024).decode("utf-8")
                    if not data:
                        print(f"[INFO] O cliente {client_address} desconectou sem enviar dados.")
                        continue
                    self._process_request(client_socket, client_address, data)
                except Exception as e:
                    print(f"[ERRO] Ocorreu um erro inesperado com {client_address}: {e}")
                finally:
                    print(f"[DESCONECTADO] A conexão com {client_address} foi encerrada.")

if __name__ == "__main__":
    server = CalculatorServer()
    server.start()
