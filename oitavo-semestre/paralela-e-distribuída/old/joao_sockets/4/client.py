import socket

class TriviaClient:
    HOST = '127.0.0.1'
    PORT = 12347

    def __init__(self):
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Conectando ao servidor de Trivia...")
            self.client_socket.connect((self.HOST, self.PORT))
            return True
        except ConnectionRefusedError:
            print("\n[ERRO] Não foi possível se conectar ao servidor. Por favor, verifique se ele está ativo e tente novamente.")
            return False
        except Exception as e:
            print(f"\n[ERRO] Ocorreu um problema inesperado ao conectar: {e}")
            return False

    def get_question_and_options(self):
        try:
            data = self.client_socket.recv(4096).decode('utf-8')
            parts = data.split('|')
            if len(parts) != 2:
                print("[ERRO] O formato da pergunta recebida do servidor é inválido.")
                return None, None
            return parts[0], parts[1].split(';')
        except Exception as e:
            print(f"[ERRO] Ocorreu um problema ao receber a pergunta: {e}")
            return None, None

    def display_question(self, question, options):
        print("\n" + "="*30)
        print("Pergunta:", question)
        print("-" * 30)
        for option in options:
            print(option)
        print("="*30)

    def send_answer(self, answer):
        try:
            self.client_socket.sendall(answer.encode('utf-8'))
            return True
        except Exception as e:
            print(f"[ERRO] Ocorreu um problema ao enviar a resposta: {e}")
            return False

    def get_feedback(self):
        try:
            feedback = self.client_socket.recv(1024).decode('utf-8')
            print(f"\n>> Feedback do servidor: {feedback}")
            return True
        except Exception as e:
            print(f"[ERRO] Ocorreu um problema ao receber o feedback: {e}")
            return False

    def close(self):
        if self.client_socket:
            self.client_socket.close()

def main():
    client = TriviaClient()
    if client.connect():
        question, options = client.get_question_and_options()
        if question and options:
            client.display_question(question, options)
            user_answer = input("Sua resposta (A, B, C ou D): ")
            if client.send_answer(user_answer):
                client.get_feedback()
    client.close()

if __name__ == "__main__":
    main()