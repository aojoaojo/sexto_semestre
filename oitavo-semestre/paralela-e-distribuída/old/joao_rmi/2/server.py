import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import time

class BankAccount:
    def __init__(self, initial_balance=0.0):
        self.balance = initial_balance
        self.lock = threading.Lock()

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("O valor do depósito deve ser um número positivo.")
        with self.lock:
            self.balance += amount
            return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("O valor do saque deve ser um número positivo.")
        with self.lock:
            if self.balance < amount:
                raise ValueError("Saldo insuficiente para realizar o saque.")
            self.balance -= amount
            return self.balance

class BankingService(rpyc.Service):
    accounts = {}
    service_lock = threading.Lock()

    def exposed_create_account(self, client_id, initial_balance=100.0):
        with self.service_lock:
            if client_id in self.accounts:
                raise ValueError(f"A conta para o cliente '{client_id}' já existe.")
            
            new_account = BankAccount(initial_balance)
            self.accounts[client_id] = new_account
            print(f"[{time.ctime()}] Conta criada para '{client_id}' com saldo inicial de R$ {initial_balance:.2f}")
            return initial_balance

    def _get_account(self, client_id):
        with self.service_lock:
            if client_id not in self.accounts:
                raise ValueError(f"A conta para o cliente '{client_id}' não foi encontrada.")
            return self.accounts[client_id]

    def exposed_get_balance(self, client_id):
        account = self._get_account(client_id)
        with account.lock:
            balance = account.balance
            print(f"[{time.ctime()}] Saldo de R$ {balance:.2f} consultado para o cliente '{client_id}'.")
            return balance

    def exposed_deposit(self, client_id, amount):
        account = self._get_account(client_id)
        new_balance = account.deposit(amount)
        print(f"[{time.ctime()}] Depósito de R$ {amount:.2f} realizado para '{client_id}'. Novo saldo: R$ {new_balance:.2f}")
        return new_balance

    def exposed_withdraw(self, client_id, amount):
        account = self._get_account(client_id)
        new_balance = account.withdraw(amount)
        print(f"[{time.ctime()}] Saque de R$ {amount:.2f} realizado por '{client_id}'. Novo saldo: R$ {new_balance:.2f}")
        return new_balance

    def exposed_transfer(self, source_id, destination_id, amount):
        source_account = self._get_account(source_id)
        destination_account = self._get_account(destination_id)

        if amount <= 0:
            raise ValueError("O valor da transferência deve ser um número positivo.")

        # Adquirir locks em uma ordem consistente para evitar deadlocks
        locks = sorted([source_account.lock, destination_account.lock], key=id)
        with locks[0]:
            with locks[1]:
                if source_account.balance < amount:
                    raise ValueError("Saldo insuficiente na conta de origem.")
                
                source_account.balance -= amount
                destination_account.balance += amount

                print(f"[{time.ctime()}] Transferência de R$ {amount:.2f} de '{source_id}' para '{destination_id}' concluída.")
                return source_account.balance

def run_server():
    host = 'localhost'
    port = 18863
    print(f"Servidor bancário RPyC iniciado em {host}:{port}...")
    server = ThreadedServer(BankingService, port=port, hostname=host)
    server.start()

if __name__ == "__main__":
    run_server()