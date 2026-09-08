import rpyc
from rpyc.utils.server import ThreadedServer
import os
import threading
import time

class FileManager:
    _files = {}
    _lock = threading.Lock()

    @classmethod
    def get_file_lock(cls, filename):
        with cls._lock:
            if filename not in cls._files:
                cls._files[filename] = threading.Lock()
            return cls._files[filename]

class FileService(rpyc.Service):
    def exposed_read_file(self, filename):
        file_lock = FileManager.get_file_lock(filename)
        with file_lock:
            print(f"[{time.ctime()}] Lendo o arquivo '{filename}'.")
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {"success": True, "content": content}
            except FileNotFoundError:
                return {"success": False, "error": f"O arquivo '{filename}' não foi encontrado."}
            except Exception as e:
                return {"success": False, "error": f"Ocorreu um erro inesperado ao ler o arquivo: {e}"}

    def exposed_read_line(self, filename, line_number):
        file_lock = FileManager.get_file_lock(filename)
        with file_lock:
            print(f"[{time.ctime()}] Lendo a linha {line_number} do arquivo '{filename}'.")
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                if not (1 <= line_number <= len(lines)):
                    return {"success": False, "error": f"Número de linha inválido. O arquivo tem {len(lines)} linhas."}

                return {"success": True, "content": lines[line_number - 1].rstrip('\n')}
            except FileNotFoundError:
                return {"success": False, "error": f"O arquivo '{filename}' não foi encontrado."}
            except Exception as e:
                return {"success": False, "error": f"Ocorreu um erro inesperado ao ler a linha: {e}"}

    def exposed_append_to_file(self, filename, content):
        file_lock = FileManager.get_file_lock(filename)
        with file_lock:
            print(f"[{time.ctime()}] Adicionando conteúdo ao arquivo '{filename}'.")
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(content)
                    if not content.endswith('\n'):
                        f.write('\n')
                return {"success": True, "message": f"Conteúdo adicionado com sucesso ao arquivo '{filename}'."}
            except Exception as e:
                return {"success": False, "error": f"Ocorreu um erro inesperado ao escrever no arquivo: {e}"}

    def exposed_delete_file(self, filename):
        file_lock = FileManager.get_file_lock(filename)
        with file_lock:
            print(f"[{time.ctime()}] Removendo o arquivo '{filename}'.")
            try:
                if not os.path.exists(filename):
                    raise FileNotFoundError
                os.remove(filename)
                return {"success": True, "message": f"Arquivo '{filename}' foi removido com sucesso."}
            except FileNotFoundError:
                return {"success": False, "error": f"O arquivo '{filename}' não foi encontrado para exclusão."}
            except Exception as e:
                return {"success": False, "error": f"Ocorreu um erro inesperado ao remover o arquivo: {e}"}

def run_server():
    host = 'localhost'
    port = 18861
    print(f"Servidor de arquivos RPyC iniciado em {host}:{port}...")
    server = ThreadedServer(FileService, port=port, hostname=host)
    server.start()

if __name__ == "__main__":
    run_server()