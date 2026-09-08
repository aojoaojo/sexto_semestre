import rpyc
import threading
import time


def client_one_simulation():
    try:
        connection = rpyc.connect("localhost", 18862)

        try:
            balance = connection.root.create_account("1", 100.0)
            print(
                f"[Cliente 1] Conta criada com sucesso. Saldo inicial: R$ {balance:.2f}"
            )
        except Exception as e:
            print(f"[Cliente 1] Erro ao criar a conta: {e}")

        time.sleep(2)

        try:
            new_balance = connection.root.transfer("1", "2", 15.0)
            print(
                f"[Cliente 1] Transferência de R$ 15.00 para o cliente 2 realizada com sucesso."
            )
            print(f"[Cliente 1] Novo saldo: R$ {new_balance:.2f}")
        except Exception as e:
            print(f"[Cliente 1] Erro durante a transferência: {e}")

        connection.close()
    except Exception as e:
        print(f"[Cliente 1] Erro de conexão: {e}")


def client_two_simulation():
    try:
        connection = rpyc.connect("localhost", 18862)

        time.sleep(1)
        try:
            balance = connection.root.create_account("2", 100.0)
            print(
                f"[Cliente 2] Conta criada com sucesso. Saldo inicial: R$ {balance:.2f}"
            )
        except Exception as e:
            print(f"[Cliente 2] Erro ao criar a conta: {e}")

        time.sleep(2)

        try:
            balance = connection.root.get_balance("2")
            print(
                f"[Cliente 2] Saldo consultado após a transferência: R$ {balance:.2f}"
            )
        except Exception as e:
            print(f"[Cliente 2] Erro ao consultar o saldo: {e}")

        connection.close()
    except Exception as e:
        print(f"[Cliente 2] Erro de conexão: {e}")


if __name__ == "__main__":
    print("=== INICIANDO TESTE DE TRANSFERÊNCIA SIMULTÂNEA ENTRE CLIENTES ===\n")

    thread1 = threading.Thread(target=client_one_simulation)
    thread2 = threading.Thread(target=client_two_simulation)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("\n=== TESTE DE TRANSFERÊNCIA CONCLUÍDO ===")
