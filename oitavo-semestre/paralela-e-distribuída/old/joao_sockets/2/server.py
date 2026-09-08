import socket
import random
import threading

class FortuneServer:
    HOST = '127.0.0.1'
    PORT = 12345
    FORTUNES = [
        "A sorte favorece os bravos.",
        "Um novo começo trará grande sucesso.",
        "A paciência é uma virtude que leva à vitória.",
        "Sua criatividade o levará a lugares inesperados.",
        "Grandes oportunidades estão a caminho.",
        "Aprenda com o passado, viva o presente e planeje o futuro.",
        "Um sorriso é a chave que abre muitas portas.",
        "A jornada de mil milhas começa com um único passo.",
        "A persistência é o caminho do êxito.",
        "Grandes realizações exigem tempo e dedicação.",
        "O otimismo é a fé que leva à realização.",
        "Sua determinação será recompensada.",
        "O sucesso está na jornada, não apenas no destino.",
        "Boas energias o aguardam no futuro próximo.",
        "Seja a mudança que você deseja ver no mundo.",
        "O momento de agir é agora."
    ]

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _handle_client_connection(self, client_socket, client_address):
        print(f"[CONEXÃO] Nova conexão estabelecida com {client_address}")
        try:
            with client_socket:
                fortune_message = random.choice(self.FORTUNES)
                client_socket.sendall(fortune_message.encode('utf-8'))
        except Exception as e:
            print(f"[ERRO] Ocorreu um erro com o cliente {client_address}: {e}")
        finally:
            print(f"[DESCONECTADO] A conexão com {client_address} foi encerrada.")

    def start(self):
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        print(f"[SERVIDOR] Servidor de mensagens da sorte iniciado na porta {self.PORT}. Aguardando conexões...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            
            thread = threading.Thread(target=self._handle_client_connection, args=(client_socket, client_address))
            thread.start()
            print(f"[INFO] Número de clientes ativos: {threading.active_count() - 1}")

if __name__ == "__main__":
    server = FortuneServer()
    server.start()