import pygame
import sys
import socket
import json
import time

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT_NUM = 65432

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_W = 10
PADDLE_H = 100
BALL_DIAMETER = 15
PADDLE_MOVE_SPEED = 9

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (200, 200, 200)

pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong Online")
game_clock = pygame.time.Clock()
main_font = pygame.font.Font(None, 74)
status_font = pygame.font.Font(None, 36)
helper_font = pygame.font.Font(None, 28)

client_id = None
game_state_from_server = {
    "p1_y": WINDOW_HEIGHT / 2,
    "p2_y": WINDOW_HEIGHT / 2,
    "ball_x": WINDOW_WIDTH / 2,
    "ball_y": WINDOW_HEIGHT / 2,
    "s1": 0, "s2": 0, "status": "waiting",
    "countdown_ms_left": 0
}

current_render_state = game_state_from_server.copy()

local_paddle_y = WINDOW_HEIGHT / 2 - PADDLE_H / 2
last_input_timestamp = 0
INPUT_SEND_RATE = 30
CONNECTION_RETRY_DELAY = 800
last_connection_attempt = 0

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setblocking(False)

def render_text(text, font, color, surface, x, y, is_centered=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if is_centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def attempt_connection():
    global last_connection_attempt
    current_time_ms = int(time.time() * 1000)
    if client_id is None and current_time_ms - last_connection_attempt > CONNECTION_RETRY_DELAY:
        udp_socket.sendto(json.dumps({"action": "hello"}).encode(), (SERVER_ADDRESS, SERVER_PORT_NUM))
        last_connection_attempt = current_time_ms

def send_player_movement():
    global last_input_timestamp
    current_time_ms = int(time.time() * 1000)
    if current_time_ms - last_input_timestamp < (1000 / INPUT_SEND_RATE):
        return
    payload = {"action": "move", "y": local_paddle_y + PADDLE_H / 2}
    udp_socket.sendto(json.dumps(payload).encode(), (SERVER_ADDRESS, SERVER_PORT_NUM))
    last_input_timestamp = current_time_ms

def linear_interpolate(start, end, alpha):
    return start + (end - start) * alpha

def update_render_state(alpha=0.2):
    for key in ("p1_y", "p2_y", "ball_x", "ball_y"):
        current_render_state[key] = linear_interpolate(current_render_state.get(key, game_state_from_server[key]), game_state_from_server[key], alpha)
    for key in ("s1", "s2", "status", "countdown_ms_left"):
        current_render_state[key] = game_state_from_server[key]

print("Tentando conectar ao servidor...")

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    attempt_connection()

    pressed_keys = pygame.key.get_pressed()
    if client_id in (1, 2):
        if (client_id == 1 and pressed_keys[pygame.K_w]) or (client_id == 2 and pressed_keys[pygame.K_UP]):
            local_paddle_y -= PADDLE_MOVE_SPEED
        if (client_id == 1 and pressed_keys[pygame.K_s]) or (client_id == 2 and pressed_keys[pygame.K_DOWN]):
            local_paddle_y += PADDLE_MOVE_SPEED
        local_paddle_y = max(0, min(WINDOW_HEIGHT - PADDLE_H, local_paddle_y))
        send_player_movement()

    try:
        while True:
            data, _ = udp_socket.recvfrom(2048)
            message = json.loads(data.decode())
            if "player_id" in message and client_id is None:
                client_id = message["player_id"]
                pygame.display.set_caption(f"Pong Online - Jogador {client_id}")
                print(f"Conectado! Você é o Jogador {client_id}.")
            else:
                game_state_from_server.update(message)
    except BlockingIOError:
        pass
    except Exception:
        pass

    interpolation_factor = 0.18 if game_state_from_server["status"] == "playing" else 0.3
    update_render_state(alpha=interpolation_factor)

    display_surface.fill(COLOR_BLACK)

    game_status = current_render_state["status"]
    player1_rect = pygame.Rect(10, current_render_state["p1_y"] - PADDLE_H / 2, PADDLE_W, PADDLE_H)
    player2_rect = pygame.Rect(WINDOW_WIDTH - 10 - PADDLE_W, current_render_state["p2_y"] - PADDLE_H / 2, PADDLE_W, PADDLE_H)
    ball_rect = pygame.Rect(current_render_state["ball_x"] - BALL_DIAMETER / 2, current_render_state["ball_y"] - BALL_DIAMETER / 2, BALL_DIAMETER, BALL_DIAMETER)

    pygame.draw.rect(display_surface, COLOR_WHITE, player1_rect)
    pygame.draw.rect(display_surface, COLOR_WHITE, player2_rect)
    pygame.draw.ellipse(display_surface, COLOR_WHITE, ball_rect)
    pygame.draw.aaline(display_surface, COLOR_WHITE, (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT))

    render_text(str(current_render_state["s1"]), main_font, COLOR_WHITE, display_surface, WINDOW_WIDTH / 4, 60)
    render_text(str(current_render_state["s2"]), main_font, COLOR_WHITE, display_surface, WINDOW_WIDTH * 3 / 4, 60)

    if game_status == "waiting":
        render_text("Aguardando oponente...", status_font, COLOR_WHITE, display_surface, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    elif game_status == "countdown":
        milliseconds_left = int(current_render_state.get("countdown_ms_left", 0))
        countdown_text = "3" if milliseconds_left > 800 else "2" if milliseconds_left > 400 else "1"
        render_text(countdown_text, main_font, COLOR_GRAY, display_surface, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    elif game_status == "game_over":
        winner = 1 if game_state_from_server.get("s1", 0) >= 10 else 2
        render_text(f"Jogador {winner} venceu!", status_font, COLOR_WHITE, display_surface, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 30)
        render_text("Reinicie o servidor para nova partida", helper_font, COLOR_GRAY, display_surface, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 10)

    if client_id == 1:
        render_text("W/S para mover", helper_font, COLOR_GRAY, display_surface, 10, WINDOW_HEIGHT - 28, is_centered=False)
    elif client_id == 2:
        render_text("↑/↓ para mover", helper_font, COLOR_GRAY, display_surface, 10, WINDOW_HEIGHT - 28, is_centered=False)
    else:
        render_text("Conectando...", helper_font, COLOR_GRAY, display_surface, 10, WINDOW_HEIGHT - 28, is_centered=False)

    pygame.display.flip()
    game_clock.tick(60)

pygame.quit()
sys.exit()