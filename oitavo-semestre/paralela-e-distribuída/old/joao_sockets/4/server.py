import socket
import random

class TriviaServer:
    HOST = '127.0.0.1'
    PORT = 12347
    QUESTIONS = [
        {
            "question": "Qual destes planetas é conhecido como 'Planeta Vermelho'?",
            "options": ["A) Vênus", "B) Marte", "C) Júpiter", "D) Saturno"],
            "answer": "B"
        },
        {
            "question": "Qual é a capital da França?",
            "options": ["A) Londres", "B) Madri", "C) Berlim", "D) Paris"],
            "answer": "D"
        },
        {
            "question": "Qual animal é conhecido como o 'rei da selva'?",
            "options": ["A) Tigre", "B) Elefante", "C) Leão", "D) Urso"],
            "answer": "C"
        },
        {
            "question": "Qual o valor de 8 x 7?",
            "options": ["A) 56", "B) 64", "C) 49", "D) 63"],
            "answer": "A"
        },
        {
            "question": "Em que ano começou a Segunda Guerra Mundial?",
            "options": ["A) 1935", "B) 1939", "C) 1941", "D) 1945"],
            "answer": "B"
        },
        {
            "question": "Qual é o maior oceano do mundo?",
            "options": ["A) Atlântico", "B) Índico", "C) Pacífico", "D) Ártico"],
            "answer": "C"
        },
        {
            "question": "Quem pintou a Mona Lisa?",
            "options": ["A) Van Gogh", "B) Picasso", "C) Da Vinci", "D) Michelangelo"],
            "answer": "C"
        },
        {
            "question": "Qual é o elemento químico mais abundante no universo?",
            "options": ["A) Oxigênio", "B) Carbono", "C) Hélio", "D) Hidrogênio"],
            "answer": "D"
        }
    ]

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _handle_client_connection(self, client_socket, client_address):
        print(f"[CONEXÃO] Novo jogador conectado de {client_address}")
        with client_socket:
            try:
                chosen_question = random.choice(self.QUESTIONS)
                question_text = chosen_question["question"]
                options_text = ";".join(chosen_question["options"])
                correct_answer = chosen_question["answer"]
                
                message_to_client = f"{question_text}|{options_text}"

                client_socket.sendall(message_to_client.encode('utf-8'))

                client_answer = client_socket.recv(1024).decode('utf-8').strip().upper()
                print(f"[RESPOSTA] O jogador de {client_address} respondeu: '{client_answer}'")

                if client_answer == correct_answer:
                    feedback = "Acertou!"
                else:
                    feedback = f"Errou, a resposta correta era {correct_answer}"

                client_socket.sendall(feedback.encode('utf-8'))
            except Exception as e:
                print(f"[ERRO] Ocorreu um erro durante a comunicação com {client_address}: {e}")
            finally:
                print(f"[DESCONECTADO] O jogador de {client_address} foi desconectado.")

    def start(self):
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        print(f"[SERVIDOR] Servidor de Trivia iniciado na porta {self.PORT}. Aguardando jogadores...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            self._handle_client_connection(client_socket, client_address)

if __name__ == "__main__":
    server = TriviaServer()
    server.start()