import rpyc
from rpyc.utils.server import ThreadedServer
from forex_python.converter import CurrencyRates

class CurrencyService(rpyc.Service):
    def exposed_get_greeting(self, name):
        return f"Olá, {name}! Esta é uma saudação do servidor."

    def exposed_convert(self, currency_from, currency_to, amount):
        currency_rates = CurrencyRates()
        return currency_rates.convert(currency_from, currency_to, amount)

if __name__ == "__main__":
    print("Servidor de conversão de moeda iniciado na porta 18861...")
    server = ThreadedServer(CurrencyService, port=18861)
    server.start()