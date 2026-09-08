import rpyc
import sys

def display_menu():
    print("\n" + "=" * 50)
    print("GERENCIADOR DE ARQUIVOS REMOTOS")
    print("=" * 50)
    print("1. Ler um arquivo completo")
    print("2. Ler uma linha específica de um arquivo")
    print("3. Adicionar conteúdo a um arquivo")
    print("4. Apagar um arquivo")
    print("5. Sair")
    print("=" * 50)

def get_line_number():
    while True:
        try:
            num = int(input("Digite o número da linha: "))
            if num > 0:
                return num
            else:
                print("O número da linha deve ser um inteiro positivo.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

def handle_read_file(connection):
    filename = input("Digite o nome do arquivo para leitura: ")
    if not filename:
        print("O nome do arquivo não pode ser vazio.")
        return
    
    result = connection.root.read_file(filename)
    if result["success"]:
        print(f"\n--- Conteúdo do arquivo: {filename} ---")
        print(result["content"])
        print("-" * (28 + len(filename)))
    else:
        print(f"\nErro ao ler o arquivo: {result['error']}")

def handle_read_line(connection):
    filename = input("Digite o nome do arquivo para leitura da linha: ")
    if not filename:
        print("O nome do arquivo não pode ser vazio.")
        return

    line_num = get_line_number()
    result = connection.root.read_line(filename, line_num)
    if result["success"]:
        print(f"\nConteúdo da linha {line_num} de '{filename}':")
        print(f"> {result['content']}")
    else:
        print(f"\nErro ao ler a linha: {result['error']}")

def handle_append_to_file(connection):
    filename = input("Digite o nome do arquivo para adicionar conteúdo: ")
    if not filename:
        print("O nome do arquivo não pode ser vazio.")
        return

    content = input("Digite o conteúdo a ser adicionado: ")
    result = connection.root.append_to_file(filename, content)
    if result["success"]:
        print(f"\n{result['message']}")
    else:
        print(f"\nErro ao adicionar conteúdo: {result['error']}")

def handle_delete_file(connection):
    filename = input("Digite o nome do arquivo a ser apagado: ")
    if not filename:
        print("O nome do arquivo não pode ser vazio.")
        return

    confirmation = input(f"Tem certeza que deseja apagar permanentemente o arquivo '{filename}'? (s/n): ")
    if confirmation.lower() == 's':
        result = connection.root.delete_file(filename)
        if result["success"]:
            print(f"\n{result['message']}")
        else:
            print(f"\nErro ao apagar o arquivo: {result['error']}")
    else:
        print("\nOperação de exclusão cancelada pelo usuário.")

def run_client():
    connection = None
    try:
        print("Conectando ao servidor de arquivos...")
        connection = rpyc.connect("localhost", 18861)
        print("Conexão estabelecida com sucesso!\n")

        action_map = {
            "1": handle_read_file,
            "2": handle_read_line,
            "3": handle_append_to_file,
            "4": handle_delete_file,
        }

        while True:
            display_menu()
            choice = input("\nEscolha uma opção do menu: ")

            if choice in action_map:
                action_map[choice](connection)
            elif choice == "5":
                print("\nEncerrando o cliente. Até logo!")
                break
            else:
                print("\nOpção inválida. Por favor, escolha uma das opções do menu.")

    except ConnectionRefusedError:
        print("\nErro fatal: A conexão com o servidor foi recusada.")
        print("Por favor, verifique se o servidor está em execução na porta correta.")
        sys.exit(1)
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    run_client()