import threading
import math


def count_word_in_chunk(
    text_chunk: str, target_word: str, worker_id: int, results_list: list
):
    count = text_chunk.count(target_word)
    print(f"Thread {worker_id}: Encontrou {count} ocorrências.")
    results_list[worker_id] = count


def main():
    source_text = input("Digite um texto: ")
    target_word = input("Digite uma palavra para ser buscada: ")

    try:
        num_chunks = int(
            input("Digite o número de blocos em que deseja dividir a busca: ")
        )
        if num_chunks <= 0:
            print("Erro.")
            return
    except ValueError:
        print("Erro.")
        return

    if not source_text or not target_word:
        print("Erro.")
        return

    worker_threads = []
    results = [0] * num_chunks
    text_length = len(source_text)
    chunk_size = text_length // num_chunks

    print(f"\nIniciando a busca em {num_chunks} threads...")

    for i in range(num_chunks):
        start_index = i * chunk_size

        if i == num_chunks - 1:
            end_index = text_length
        else:
            end_index = start_index + chunk_size

        text_chunk = source_text[start_index:end_index]

        worker = threading.Thread(
            target=count_word_in_chunk, args=(text_chunk, target_word, i, results)
        )
        worker_threads.append(worker)
        worker.start()

    for worker in worker_threads:
        worker.join()

    total_count = sum(results)

    print("\nFim da Busca.")
    print(
        f"A palavra '{target_word}' foi encontrada um total de {total_count} vezes no texto."
    )


if __name__ == "__main__":
    main()
