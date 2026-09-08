import socket

class CalculatorClient:
    HOST = '127.0.0.1'
    PORT = 12346

    def __init__(self):
        self.client_socket = None

    @staticmethod
    def _get_float_input(prompt_message):
        while True:
            try:
                return float(input(prompt_message))
            except ValueError:
                print("[ENTRADA INVÁLIDA] Por favor, digite um número válido.")

    def _display_menu(self):
        print("\n--- Calculadora Remota TCP ---")
        print("1. Soma")
        print("2. Subtração")
        print("3. Multiplicação")
        print("4. Divisão")
        print("5. Sair")

    def run(self):
        while True:
            self._display_menu()
            user_choice = input("Escolha uma opção (1-5): ")

            if user_choice == '5':
                print("Encerrando a calculadora remota.")
                break
            
            if user_choice not in ['1', '2', '3', '4']:
                print("[OPÇÃO INVÁLIDA] Por favor, escolha uma opção de 1 a 5.")
                continue

            first_number = self._get_float_input("Digite o primeiro número: ")
            second_number = self._get_float_input("Digite o segundo número: ")

            operations_map = {
                '1': 'SOMA',
                '2': 'SUBTRACAO',
                '3': 'MULTIPLICACAO',
                '4': 'DIVISAO'
            }
            operation_name = operations_map[user_choice]
            
            message_to_server = f"{operation_name};{first_number};{second_number}"

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((self.HOST, self.PORT))
                    client_socket.sendall(message_to_server.encode('utf-8'))
                    server_response = client_socket.recv(1024).decode('utf-8')
                    
                    print("-" * 30)
                    print(f"Resultado do servidor: {server_response}")
                    print("-" * 30)

            except ConnectionRefusedError:
                print("\n[ERRO] Não foi possível se conectar ao servidor. Verifique se ele está ativo.")
            except Exception as e:
                print(f"\n[ERRO] Ocorreu um problema inesperado na comunicação: {e}")

if __name__ == "__main__":
    client = CalculatorClient()
    client.run()