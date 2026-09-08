import rpyc

def run_client():
    try:
        connection = rpyc.connect("localhost", 18861)

        print("--- Testando Chamadas Remotas ---")

        # Teste 1: Saudação
        name = "Michelangelo"
        greeting = connection.root.get_greeting(name)
        print(f"Saudação para '{name}': {greeting}")

        # Teste 2: Conversão de Moeda
        amount_to_convert = 100
        source_currency = "USD"
        target_currency = "BRL"
        result = connection.root.convert(source_currency, target_currency, amount_to_convert)
        print(f"Conversão de {amount_to_convert} {source_currency} para {target_currency}: {result:.2f} {target_currency}")

        connection.close()
        print("\nConexão com o servidor foi fechada.")

    except ConnectionRefusedError:
        print("\nErro: A conexão com o servidor RPyC foi recusada.")
        print("Por favor, verifique se o servidor está em execução na porta 18861.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

if __name__ == "__main__":
    run_client()