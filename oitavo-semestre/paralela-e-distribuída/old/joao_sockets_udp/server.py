import socket
import json
import time
import random
import math

HOST_IP = "127.0.0.1"
LISTENING_PORT = 65432
MAX_CLIENTS = 2
SCORE_TO_WIN = 10

SIMULATION_TICK_RATE = 120
NETWORK_UPDATE_RATE = 30
ROUND_START_DELAY = 1200

FIELD_WIDTH = 800
FIELD_HEIGHT = 600
PADDLE_GRAPHIC_WIDTH = 10
PADDLE_GRAPHIC_HEIGHT = 100
BALL_GRAPHIC_DIAMETER = 15

BALL_START_SPEED = 7.0
BALL_SPEED_MULTIPLIER = 1.05
BALL_MAX_SPEED = 18.0
BALL_WALL_BOUNCE_DAMPING = 1.0

connected_players = {}
paddles_state = {1: {"y": FIELD_HEIGHT / 2}, 2: {"y": FIELD_HEIGHT / 2}}
ball_position = {"x": FIELD_WIDTH / 2, "y": FIELD_HEIGHT / 2}
ball_velocity = {"x": 0.0, "y": 0.0}
player_scores = {1: 0, 2: 0}
game_phase = "waiting"
next_round_start_time = 0


def get_current_milliseconds():
    return int(time.time() * 1000)


def clamp_value(value, min_val, max_val):
    return max(min_val, min(max_val, value))


def reset_ball_position(direction_multiplier):
    ball_position["x"] = FIELD_WIDTH / 2
    ball_position["y"] = FIELD_HEIGHT / 2
    angle = random.uniform(-0.35, 0.35)
    speed = BALL_START_SPEED
    ball_velocity["x"] = math.copysign(speed * math.cos(angle), direction_multiplier)
    ball_velocity["y"] = speed * math.sin(angle)


def begin_new_round(direction_multiplier):
    global game_phase, next_round_start_time
    reset_ball_position(direction_multiplier)
    game_phase = "countdown"
    next_round_start_time = get_current_milliseconds() + ROUND_START_DELAY


def check_paddle_collision(ball_r, paddle_r):
    bx, by, bw, bh = ball_r
    px, py, pw, ph = paddle_r
    return bx < px + pw and bx + bw > px and by < py + ph and by + bh > py


def tick_game_simulation(delta_time):
    global game_phase

    if game_phase == "countdown":
        if get_current_milliseconds() >= next_round_start_time:
            game_phase = "playing"
        else:
            return
    if game_phase != "playing":
        return

    ball_position["x"] += ball_velocity["x"] * delta_time * 60.0
    ball_position["y"] += ball_velocity["y"] * delta_time * 60.0

    half_ball_size = BALL_GRAPHIC_DIAMETER / 2
    if ball_position["y"] - half_ball_size <= 0:
        ball_position["y"] = half_ball_size
        ball_velocity["y"] = -ball_velocity["y"] * BALL_WALL_BOUNCE_DAMPING
    elif ball_position["y"] + half_ball_size >= FIELD_HEIGHT:
        ball_position["y"] = FIELD_HEIGHT - half_ball_size
        ball_velocity["y"] = -ball_velocity["y"] * BALL_WALL_BOUNCE_DAMPING

    player1_y = paddles_state[1]["y"]
    player2_y = paddles_state[2]["y"]
    player1_rect = (
        10,
        player1_y - PADDLE_GRAPHIC_HEIGHT / 2,
        PADDLE_GRAPHIC_WIDTH,
        PADDLE_GRAPHIC_HEIGHT,
    )
    player2_rect = (
        FIELD_WIDTH - 10 - PADDLE_GRAPHIC_WIDTH,
        player2_y - PADDLE_GRAPHIC_HEIGHT / 2,
        PADDLE_GRAPHIC_WIDTH,
        PADDLE_GRAPHIC_HEIGHT,
    )
    ball_rect = (
        ball_position["x"] - half_ball_size,
        ball_position["y"] - half_ball_size,
        BALL_GRAPHIC_DIAMETER,
        BALL_GRAPHIC_DIAMETER,
    )

    def handle_paddle_bounce(is_left_paddle):
        nonlocal ball_rect
        if is_left_paddle:
            ball_position["x"] = 10 + PADDLE_GRAPHIC_WIDTH + half_ball_size
        else:
            ball_position["x"] = (
                FIELD_WIDTH - 10 - PADDLE_GRAPHIC_WIDTH - half_ball_size
            )

        paddle_y = player1_y if is_left_paddle else player2_y
        bounce_offset = (ball_position["y"] - paddle_y) / (PADDLE_GRAPHIC_HEIGHT / 2)
        bounce_offset = clamp_value(bounce_offset, -1, 1)

        new_speed = min(
            BALL_MAX_SPEED,
            math.hypot(ball_velocity["x"], ball_velocity["y"]) * BALL_SPEED_MULTIPLIER,
        )
        bounce_angle = bounce_offset * 0.7
        direction_x = 1 if not is_left_paddle else -1
        ball_velocity["x"] = direction_x * new_speed * math.cos(bounce_angle)
        ball_velocity["y"] = new_speed * math.sin(bounce_angle)

    if ball_velocity["x"] < 0 and check_paddle_collision(ball_rect, player1_rect):
        handle_paddle_bounce(is_left_paddle=True)
    elif ball_velocity["x"] > 0 and check_paddle_collision(ball_rect, player2_rect):
        handle_paddle_bounce(is_left_paddle=False)

    if ball_position["x"] + half_ball_size < 0:
        player_scores[2] += 1
        if player_scores[2] >= SCORE_TO_WIN:
            game_phase = "game_over"
        else:
            begin_new_round(direction_multiplier=1)
    elif ball_position["x"] - half_ball_size > FIELD_WIDTH:
        player_scores[1] += 1
        if player_scores[1] >= SCORE_TO_WIN:
            game_phase = "game_over"
        else:
            begin_new_round(direction_multiplier=-1)


def create_game_state_payload():
    return {
        "p1_y": paddles_state[1]["y"],
        "p2_y": paddles_state[2]["y"],
        "ball_x": ball_position["x"],
        "ball_y": ball_position["y"],
        "s1": player_scores[1],
        "s2": player_scores[2],
        "status": game_phase,
        "server_ms": get_current_milliseconds(),
        "countdown_ms_left": (
            max(0, next_round_start_time - get_current_milliseconds())
            if game_phase == "countdown"
            else 0
        ),
    }


def register_player(player_address):
    if player_address in connected_players:
        return connected_players[player_address]
    if len(connected_players) < MAX_CLIENTS:
        player_id = len(connected_players) + 1
        connected_players[player_address] = player_id
        return player_id
    return None


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST_IP, LISTENING_PORT))
    server_socket.setblocking(False)
    print(f"Servidor do jogo ouvindo em {HOST_IP}:{LISTENING_PORT}")

    last_tick_time = time.perf_counter()
    last_broadcast_time = 0.0

    while True:
        try:
            while True:
                received_data, address = server_socket.recvfrom(1024)
                message = json.loads(received_data.decode())
                action = message.get("action", "")

                if action in ("hello", "connect"):
                    player_id = register_player(address)
                    if player_id is not None:
                        server_socket.sendto(
                            json.dumps({"player_id": player_id}).encode(), address
                        )
                        if (
                            len(connected_players) == MAX_CLIENTS
                            and game_phase == "waiting"
                        ):
                            begin_new_round(direction_multiplier=random.choice((1, -1)))
                            print("Jogo iniciado!")
                elif action == "move" and address in connected_players:
                    player_id = connected_players[address]
                    paddle_y_position = float(message.get("y", FIELD_HEIGHT / 2))
                    paddle_y_position = clamp_value(
                        paddle_y_position,
                        PADDLE_GRAPHIC_HEIGHT / 2,
                        FIELD_HEIGHT - PADDLE_GRAPHIC_HEIGHT / 2,
                    )
                    paddles_state[player_id]["y"] = paddle_y_position
        except BlockingIOError:
            pass
        except Exception:
            pass

        current_time = time.perf_counter()
        delta_time = current_time - last_tick_time
        time_step = 1.0 / SIMULATION_TICK_RATE
        while delta_time >= time_step:
            tick_game_simulation(time_step)
            delta_time -= time_step
            last_tick_time += time_step

        if current_time - last_broadcast_time >= 1.0 / NETWORK_UPDATE_RATE:
            game_state_payload = create_game_state_payload()
            payload_data = json.dumps(game_state_payload).encode()
            for addr in list(connected_players.keys()):
                try:
                    server_socket.sendto(payload_data, addr)
                except OSError:
                    pass
            last_broadcast_time = current_time

        time.sleep(0.001)
