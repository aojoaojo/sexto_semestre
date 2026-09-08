import rpyc
import sys

def display_menu():
    print("\n--- Menu Principal ---")
    print("1. Consultar saldo")
    print("2. Realizar um depósito")
    print("3. Efetuar um saque")
    print("4. Fazer uma transferência")
    print("9. Sair")

def get_numeric_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("O valor deve ser um número positivo. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def handle_get_balance(connection, client_id):
    try:
        balance = connection.root.get_balance(client_id)
        print(f"\nO seu saldo atual é: R$ {balance:.2f}")
    except Exception as e:
        print(f"\nErro ao consultar o saldo: {e}")

def handle_deposit(connection, client_id):
    amount = get_numeric_input("Digite o valor a ser depositado: R$ ")
    try:
        new_balance = connection.root.deposit(client_id, amount)
        print(f"Depósito realizado com sucesso! Seu novo saldo é: R$ {new_balance:.2f}")
    except Exception as e:
        print(f"\nErro ao realizar o depósito: {e}")

def handle_withdraw(connection, client_id):
    amount = get_numeric_input("Digite o valor a ser sacado: R$ ")
    try:
        new_balance = connection.root.withdraw(client_id, amount)
        print(f"Saque efetuado com sucesso! Seu novo saldo é: R$ {new_balance:.2f}")
    except Exception as e:
        print(f"\nErro ao efetuar o saque: {e}")

def handle_transfer(connection, client_id):
    destination_id = input("Digite o ID da conta de destino: ")
    if not destination_id:
        print("O ID de destino não pode ser vazio.")
        return
    
    amount = get_numeric_input("Digite o valor a ser transferido: R$ ")
    try:
        new_balance = connection.root.transfer(client_id, destination_id, amount)
        print(f"Transferência para '{destination_id}' realizada com sucesso! Seu novo saldo é: R$ {new_balance:.2f}")
    except Exception as e:
        print(f"\nErro ao realizar a transferência: {e}")

def run_client():
    connection = None
    try:
        connection = rpyc.connect('localhost', 18863)
        print("=== Bem-vindo ao Cliente Bancário ===")
        
        client_id = input("Para começar, digite seu ID de cliente: ")
        if not client_id:
            print("O ID do cliente não pode ser vazio. Encerrando.")
            return

        try:
            initial_balance = connection.root.create_account(client_id)
            print(f"Conta '{client_id}' criada com sucesso! Saldo inicial: R$ {initial_balance:.2f}")
        except Exception as e:
            print(f"Aviso: Não foi possível criar uma nova conta. {e}")
        
        while True:
            display_menu()
            option = input("Escolha uma opção: ")

            if option == "1":
                handle_get_balance(connection, client_id)
            elif option == "2":
                handle_deposit(connection, client_id)
            elif option == "3":
                handle_withdraw(connection, client_id)
            elif option == "4":
                handle_transfer(connection, client_id)
            elif option == "9":
                print("\nObrigado por usar nossos serviços. Encerrando o cliente...")
                break
            else:
                print("Opção inválida! Por favor, escolha uma das opções do menu.")
    
    except ConnectionRefusedError:
        print("Erro fatal: Não foi possível conectar ao servidor. Verifique se ele está ativo.")
        sys.exit(1)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    run_client()