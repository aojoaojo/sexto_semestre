import threading
import random
import time


def download_part(part_id: int, part_size: float, min_speed: int, max_speed: int):
    print(f"Part [{part_id}]: Download started.")

    downloaded = 0.0
    while downloaded < part_size:
        download_chunk = random.randint(min_speed, max_speed)

        downloaded = min(downloaded + download_chunk, part_size)

        print(f"Part [{part_id}]: {downloaded:.2f} / {part_size:.2f} MB")
        time.sleep(1)

    print(f"Part [{part_id}]: Download finished.")


def main():
    try:
        file_size_mb = int(input("Insira o tamanho do arquivo (MB): "))
        num_parts = int(input("Em quantas partes deseja dividí-lo? "))
        min_speed_mbps = int(input("Insira a faixa mínima de banda (MB/s): "))
        max_speed_mbps = int(input("Insira a faixa máxima de banda (MB/s): "))

        if (
            file_size_mb <= 0
            or num_parts <= 0
            or min_speed_mbps < 0
            or max_speed_mbps < min_speed_mbps
        ):
            print("Input Inválido.")
            return

    except ValueError:
        print("Input Inválido.")
        return

    threads = []
    part_size = file_size_mb / num_parts

    print(
        f"\Iniciando o download de um arquivo de {file_size_mb} MB em {num_parts} partes..."
    )
    start_time = time.time()

    # Create and start all threads
    for i in range(num_parts):
        thread = threading.Thread(
            target=download_part, args=(i, part_size, min_speed_mbps, max_speed_mbps)
        )
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete their execution
    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\Todas as partes foram baixadas com sucesso.")
    print(f"Tempo total de download: {total_time:.2f} segundos.")


if __name__ == "__main__":
    main()
