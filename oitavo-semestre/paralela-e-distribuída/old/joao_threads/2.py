import threading
import random
import time
import queue
from datetime import datetime
from itertools import cycle


def producer(message_queue: queue.Queue, stop_event: threading.Event):
    phrases = [
        "Don't Panic.",
        "The answer to the ultimate question of life, the universe, and everything is 42.",
        "So long, and thanks for all the fish.",
        "A towel is about the most massively useful thing an interstellar hitchhiker can have.",
        "Time is an illusion. Lunchtime doubly so.",
        "The ships hung in the sky in much the same way that bricks don't.",
        "I'd far rather be happy than right any day.",
        "This must be Thursday. I never could get the hang of Thursdays.",
        "Mostly harmless.",
        "Here I am, brain the size of a planet...",
        "In the beginning, the Universe was created. This has made a lot of people very angry and has been widely regarded as a bad move.",
        "We apologize for the inconvenience.",
        "The best drink in existence is the Pan Galactic Gargle Blaster.",
        "Vogon poetry is of course the third worst in the Universe.",
        "Isn't it enough to see that a garden is beautiful without having to believe that there are fairies at the bottom of it too?",
    ]

    character_cycler = cycle(["Alfred", "Bruce"])

    while not stop_event.is_set():
        try:
            random_phrase = random.choice(phrases)
            random_sleep_time = random.uniform(0.5, 2.0)

            current_character = next(character_cycler)
            current_time = datetime.now().strftime("%H:%M:%S")

            message = f"[{current_time}] {current_character}: {random_phrase}"

            print("[PRODUTOR] --> Mensagem gerada")
            message_queue.put(message)

            time.sleep(random_sleep_time)
        except Exception as e:
            print(f"[PRODUTOR] Erro: {e}")
            break


def consumer(message_queue: queue.Queue, stop_event: threading.Event):
    while not stop_event.is_set() or not message_queue.empty():
        try:
            message = message_queue.get(timeout=1)
            print("[CONSUMIDOR] --> Mensagem recebida")
            print(f"{message}\n")
            message_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            print(f"[CONSUMIDOR] Erro: {e}")
            break


def main():
    try:
        duration_seconds = int(input("Defina a duração da interação em segundos: "))
    except ValueError:
        print("Input Inválido.")
        return

    message_queue = queue.Queue()
    stop_event = threading.Event()

    producer_thread = threading.Thread(
        target=producer, args=(message_queue, stop_event)
    )
    consumer_thread = threading.Thread(
        target=consumer, args=(message_queue, stop_event)
    )

    print("\n--- Iniciando a simulação ---")
    producer_thread.start()
    consumer_thread.start()

    time.sleep(duration_seconds)

    print("\n--- Tempo finalizado. Encerrando threads... ---")
    stop_event.set()

    producer_thread.join()
    consumer_thread.join()

    print("--- Fim da simulação ---")


if __name__ == "__main__":
    main()
