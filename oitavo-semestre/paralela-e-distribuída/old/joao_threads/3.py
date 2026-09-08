import random
import threading
import time

MIN_DURATION_MS = 500
MAX_DURATION_MS = 1000

TASK_DESCRIPTIONS = [
    "Tentar sair do Vim",
    "Centralizar uma div no CSS (tarefa impossível)",
    "Procurar o ponto e vírgula que quebrou a compilação",
    "Explicar o bug para o pato de borracha",
    "Dar 'git push --force' e torcer pelo melhor",
    "Reiniciar o roteador pela décima vez",
    "Convencer a impressora de que ela tem papel",
    "Baixar mais memória RAM da internet",
    "Evitar que a IA domine o mundo",
    "Reverter a polaridade do fluxo de nêutrons",
    "Alinhar os chakras do servidor com um backup",
    "Desfragmentar o HD da Estrela da Morte",
    "Farmar XP respondendo e-mails chatos",
    "Procurar a Toalha (a coisa mais útil do universo)",
    "Apagar o fogo no data center (de novo)",
    "Ensinar o chatbot a ter uma crise existencial",
    "Organizar a pasta de memes por ordem de importância",
    "Platinar a planilha de retrospectiva da sprint",
    "Ler todos os termos e condições (só que não)",
    "Provar para o reCAPTCHA que uma bicicleta é uma bicicleta",
    "Levar o Um Anel para a lixeira do sistema",
    "Compilar o código na sexta-feira às 17h",
    "Debater se o correto é 'GIF' ou 'JIF' com a equipe",
    "Atualizar o Java sem instalar a barra de busca do Ask",
    "Encontrar o fechamento de parênteses perdido desde 2007",
    "Fechar 3 das 174 abas abertas no Chrome",
    "Rodar um 'hello world' para se sentir produtivo",
    "Configurar a cafeteira para aceitar comandos via SSH",
    "Passar o antivírus no disquete de boot",
    "Discutir com o Clippy sobre formatação de documento",
    "Calibrar o capacitor de fluxo para a daily",
    "Verificar se a স্কynet já se tornou autoconsciente",
    "Fazer uma oferenda aos deuses do Wi-Fi",
    "Escrever documentação que alguém realmente vai ler",
    "Achar o cabo USB que funciona de primeira",
]


def perform_task(task_name: str, duration_ms: int, worker_id: int):
    start_time_str = time.strftime("%H:%M:%S")
    print(
        f"[{start_time_str}] TRABALHADOR {worker_id}: Iniciando tarefa -> {task_name} (Est. {duration_ms}ms)"
    )

    time.sleep(duration_ms / 1000)

    end_time_str = time.strftime("%H:%M:%S")
    print(
        f"[{end_time_str}] TRABALHADOR {worker_id}: Finalizando tarefa -> {task_name}"
    )


def main():
    try:
        max_concurrent_tasks = int(
            input("Quantas tarefas devem acontecer simultaneamente? ")
        )
        if max_concurrent_tasks <= 0:
            print("Input inválido.")
            return
    except ValueError:
        print("Input inválido.")
        return

    tasks = {
        name: random.randint(MIN_DURATION_MS, MAX_DURATION_MS)
        for name in TASK_DESCRIPTIONS
    }

    remaining_tasks = list(tasks.items())
    worker_id_counter = 1
    start_time = time.time()

    print(
        f"\n--- Iniciando a simulação com {len(remaining_tasks)} tarefas a serem concluídas. ---"
    )

    while remaining_tasks:
        active_batch = []
        batch_size = min(max_concurrent_tasks, len(remaining_tasks))

        print(f"\n--- Iniciando um novo lote de {batch_size} tarefas ---")

        for _ in range(batch_size):
            task_name, duration_ms = remaining_tasks.pop()
            thread = threading.Thread(
                target=perform_task, args=(task_name, duration_ms, worker_id_counter)
            )
            thread.start()
            active_batch.append(thread)
            worker_id_counter += 1

        for thread in active_batch:
            thread.join()

    total_time = time.time() - start_time
    print(f"\n--- Todas as tarefas foram concluídas em {total_time:.2f} segundos. ---")


if __name__ == "__main__":
    main()
