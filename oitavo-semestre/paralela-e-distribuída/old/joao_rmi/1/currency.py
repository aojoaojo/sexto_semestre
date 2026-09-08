import rpyc
from rpyc.utils.server import ThreadedServer

class CurrencyService(rpyc.Service):
    def exposed_get_greeting(self, name):
        return f"Olá, {name}! Esta é uma saudação do servidor."

    def exposed_sum_values(self, a, b):
        return a + b

if __name__ == "__main__":
    print("Servidor de moeda (exemplo) iniciado na porta 18861...")
    server = ThreadedServer(CurrencyService, port=18861)
    server.start()