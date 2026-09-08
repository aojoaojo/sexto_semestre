import socket
import threading
import time

class FortuneClient:
    HOST = '127.0.0.1'
    PORT = 12345
    REQUESTS_PER_CLIENT = 5
    DELAY_BETWEEN_REQUESTS = 1.5

    def __init__(self, client_id):
        self.client_id = client_id

    def make_requests(self):
        for i in range(self.REQUESTS_PER_CLIENT):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((self.HOST, self.PORT))
                    data = client_socket.recv(1024)
                    
                    current_time = time.strftime('%H:%M:%S')
                    print(f"[CLIENTE {self.client_id}] [{current_time}] Requisição {i + 1} - Mensagem recebida: {data.decode('utf-8')}")
            
            except ConnectionRefusedError:
                print(f"[CLIENTE {self.client_id}] [ERRO] Requisição {i + 1}: Não foi possível conectar. O servidor parece estar offline.")
            except Exception as e:
                print(f"[CLIENTE {self.client_id}] [ERRO] Requisição {i + 1}: Ocorreu um erro inesperado: {e}")
            
            time.sleep(self.DELAY_BETWEEN_REQUESTS)

def main():
    NUM_CLIENTS = 5
    threads = []
    
    print(f"Iniciando simulação com {NUM_CLIENTS} clientes, cada um fazendo {FortuneClient.REQUESTS_PER_CLIENT} requisições.")

    for i in range(NUM_CLIENTS):
        client = FortuneClient(i + 1)
        thread = threading.Thread(target=client.make_requests)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\nSimulação concluída. Todas as requisições dos clientes foram processadas.")

if __name__ == "__main__":
    main()