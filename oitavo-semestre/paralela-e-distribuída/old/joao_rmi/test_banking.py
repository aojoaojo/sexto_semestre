import rpyc
import sys


def run_banking_tests():
    print("=" * 60)
    print("INICIANDO TESTE AUTOMATIZADO DO SISTEMA BANCÁRIO RMI")
    print("=" * 60)

    try:
        print("\n[1] Conectando ao servidor RMI...")
        connection = rpyc.connect("localhost", 18862)
        print("✓ Conexão estabelecida com sucesso!")

        print("\n[2] Testando a criação de contas...")
        try:
            balance1 = connection.root.create_account("client_A", 100.0)
            print(f"✓ Conta 'client_A' criada com saldo inicial de: R$ {balance1:.2f}")

            balance2 = connection.root.create_account("client_B", 200.0)
            print(f"✓ Conta 'client_B' criada com saldo inicial de: R$ {balance2:.2f}")
        except Exception as e:
            print(f"✗ Erro ao criar contas: {e}")
            return False

        print("\n[3] Testando a consulta de saldo...")
        try:
            balance_a = connection.root.get_balance("client_A")
            balance_b = connection.root.get_balance("client_B")
            print(f"✓ Saldo de client_A: R$ {balance_a:.2f}")
            print(f"✓ Saldo de client_B: R$ {balance_b:.2f}")
        except Exception as e:
            print(f"✗ Erro ao consultar saldo: {e}")
            return False

        print("\n[4] Testando a operação de depósito...")
        try:
            new_balance = connection.root.deposit("client_A", 50.0)
            print(f"✓ Depósito de R$ 50.00 para client_A")
            print(f"  Novo saldo: R$ {new_balance:.2f} (Esperado: R$ 150.00)")

            if abs(new_balance - 150.0) > 0.01:
                print("✗ ERRO: Saldo incorreto após o depósito!")
                return False
        except Exception as e:
            print(f"✗ Erro ao depositar: {e}")
            return False

        print("\n[5] Testando a operação de saque...")
        try:
            new_balance = connection.root.withdraw("client_B", 30.0)
            print(f"✓ Saque de R$ 30.00 de client_B")
            print(f"  Novo saldo: R$ {new_balance:.2f} (Esperado: R$ 170.00)")

            if abs(new_balance - 170.0) > 0.01:
                print("✗ ERRO: Saldo incorreto após o saque!")
                return False
        except Exception as e:
            print(f"✗ Erro ao sacar: {e}")
            return False

        print("\n[6] Testando a operação de transferência...")
        try:
            source_balance_before = connection.root.get_balance("client_A")
            destination_balance_before = connection.root.get_balance("client_B")

            new_source_balance = connection.root.transfer("client_A", "client_B", 50.0)
            destination_balance_after = connection.root.get_balance("client_B")

            print(f"✓ Transferência de R$ 50.00 de client_A para client_B")
            print(
                f"  Saldo client_A: R$ {new_source_balance:.2f} (Esperado: R$ 100.00)"
            )
            print(
                f"  Saldo client_B: R$ {destination_balance_after:.2f} (Esperado: R$ 220.00)"
            )

            if (
                abs(new_source_balance - 100.0) > 0.01
                or abs(destination_balance_after - 220.0) > 0.01
            ):
                print("✗ ERRO: Saldos incorretos após a transferência!")
                return False
        except Exception as e:
            print(f"✗ Erro ao transferir: {e}")
            return False

        print("\n[7] Testando o tratamento de erros...")

        try:
            connection.root.create_account("client_A", 100.0)
            print("✗ ERRO: A criação de conta duplicada deveria ser impedida!")
            return False
        except Exception as e:
            print(f"✓ Bloqueio de conta duplicada funcionou como esperado: {e}")

        try:
            connection.root.get_balance("client_X")
            print("✗ ERRO: Deveria retornar um erro para cliente inexistente!")
            return False
        except Exception as e:
            print(f"✓ Detecção de cliente inexistente funcionou como esperado: {e}")

        try:
            connection.root.withdraw("client_A", 10000.0)
            print("✗ ERRO: O saque com saldo insuficiente deveria ser impedido!")
            return False
        except Exception as e:
            print(f"✓ Detecção de saldo insuficiente funcionou como esperado: {e}")

        try:
            connection.root.deposit("client_A", -50.0)
            print("✗ ERRO: O depósito de valor negativo deveria ser impedido!")
            return False
        except Exception as e:
            print(f"✓ Bloqueio de valor negativo funcionou como esperado: {e}")

        print("\n[8] Verificação final dos saldos...")
        final_balance_a = connection.root.get_balance("client_A")
        final_balance_b = connection.root.get_balance("client_B")
        print(f"✓ Saldo final de client_A: R$ {final_balance_a:.2f}")
        print(f"✓ Saldo final de client_B: R$ {final_balance_b:.2f}")

        connection.close()

        print("\n" + "=" * 60)
        print("✓ TESTES FORAM CONCLUÍDOS COM SUCESSO!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ ERRO NO TESTE: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_banking_tests()
    sys.exit(0 if success else 1)
