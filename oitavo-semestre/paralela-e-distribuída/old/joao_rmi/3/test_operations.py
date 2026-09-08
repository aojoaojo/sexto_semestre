import rpyc
import os
import sys

class FileOperationsTester:
    def __init__(self, connection):
        self.connection = connection
        self.test_file = "test_file_operations.txt"
        self.sample_file = "sample_for_tests.txt"

    def setup(self):
        print("\n--- Configurando ambiente de teste ---")
        # Cria um arquivo de exemplo para testes de leitura
        with open(self.sample_file, "w", encoding="utf-8") as f:
            f.write("Esta é a primeira linha.\n")
            f.write("Esta é a segunda linha.\n")
        print(f"Arquivo de amostra '{self.sample_file}' criado.")
        # Garante que o arquivo de teste principal não existe
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        print("Ambiente de teste pronto.")

    def teardown(self):
        print("\n--- Limpando ambiente de teste ---")
        # Remove os arquivos criados durante os testes
        for f in [self.test_file, self.sample_file]:
            if os.path.exists(f):
                os.remove(f)
                print(f"Arquivo de teste '{f}' removido.")
        print("Limpeza concluída.")

    def run(self):
        self.setup()
        try:
            self.test_append_and_read_file()
            self.test_read_line()
            self.test_delete_file()
            self.test_error_handling()
        finally:
            self.teardown()

    def test_append_and_read_file(self):
        print("\n--- Teste: Adicionar conteúdo e Ler arquivo completo ---")
        content1 = "Primeira linha de conteúdo."
        self.connection.root.append_to_file(self.test_file, content1)
        print(f"Adicionado: '{content1}'")
        content2 = "Segunda linha de conteúdo."
        self.connection.root.append_to_file(self.test_file, content2)
        print(f"Adicionado: '{content2}'")

        result = self.connection.root.read_file(self.test_file)
        expected_content = content1 + '\n' + content2 + '\n'
        assert result["success"], "A leitura do arquivo falhou"
        assert result["content"] == expected_content, "O conteúdo lido não corresponde ao esperado"
        print("✓ Teste de adição e leitura de arquivo completo passou.")

    def test_read_line(self):
        print("\n--- Teste: Leitura de linha específica ---")
        result = self.connection.root.read_line(self.sample_file, 2)
        expected_line = "Esta é a segunda linha."
        assert result["success"], "A leitura da linha falhou"
        assert result["content"] == expected_line, "O conteúdo da linha lida não corresponde ao esperado"
        print("✓ Teste de leitura de linha específica passou.")

    def test_delete_file(self):
        print("\n--- Teste: Remoção de arquivo ---")
        temp_file = "temp_delete_test.txt"
        self.connection.root.append_to_file(temp_file, "delete me")
        result = self.connection.root.delete_file(temp_file)
        assert result["success"], "A remoção do arquivo falhou"
        # Verifica localmente se o arquivo foi removido
        assert not os.path.exists(temp_file), "O arquivo não foi removido do sistema de arquivos"
        print("✓ Teste de remoção de arquivo passou.")

    def test_error_handling(self):
        print("\n--- Teste: Tratamento de Erros ---")
        # Linha fora do intervalo
        result = self.connection.root.read_line(self.sample_file, 99)
        assert not result["success"], "Esperava-se um erro para linha fora do intervalo"
        print("✓ Erro de linha fora do intervalo tratado corretamente.")

        # Arquivo inexistente
        result = self.connection.root.read_file("arquivo_que_nao_existe.txt")
        assert not result["success"], "Esperava-se um erro para arquivo inexistente"
        print("✓ Erro de arquivo inexistente tratado corretamente.")

def main():
    connection = None
    try:
        print("Conectando ao servidor para iniciar os testes...")
        connection = rpyc.connect("localhost", 18861)
        print("✓ Conexão bem-sucedida!\n")
        
        tester = FileOperationsTester(connection)
        tester.run()
        
        print("\n" + "=" * 60)
        print("RESUMO: Todos os testes foram executados com sucesso!")
        print("=" * 60)

    except ConnectionRefusedError:
        print("\n✗ Erro Crítico: Não foi possível conectar ao servidor.")
        print("  Certifique-se de que o servidor está ativo e na porta correta.")
        sys.exit(1)
    except AssertionError as e:
        print(f"\n✗ FALHA NO TESTE: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erro Inesperado durante os testes: {e}")
        sys.exit(1)
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()