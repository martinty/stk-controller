# pygame http and TCP client controller
# python -m pip install pygame
# python -m pip install requests

import argparse
import socket
from typing import Tuple

import pygame
import requests

CONTROLLER_PYGAME = {
    1: {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "right": pygame.K_RIGHT,
        "left": pygame.K_LEFT,
        "act": pygame.K_SPACE,
    },
    2: {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "right": pygame.K_d,
        "left": pygame.K_a,
        "act": pygame.K_f,
    },
    3: {
        "up": pygame.K_4,
        "down": pygame.K_r,
        "right": pygame.K_t,
        "left": pygame.K_e,
        "act": pygame.K_y,
    },
    4: {
        "up": pygame.K_u,
        "down": pygame.K_j,
        "right": pygame.K_k,
        "left": pygame.K_h,
        "act": pygame.K_l,
    },
}


def pygame_init() -> None:
    pygame.init()
    pygame.display.set_mode(size=(400, 200))


def control_player_pygame(player: int, clock: pygame.time.Clock) -> Tuple[int, int, int]:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))
    acc = dir = act = 0
    keys = pygame.key.get_pressed()
    if keys[CONTROLLER_PYGAME[player]["left"]]:
        dir = -100
    elif keys[CONTROLLER_PYGAME[player]["right"]]:
        dir = 100
    if keys[CONTROLLER_PYGAME[player]["up"]]:
        acc = 100
    elif keys[CONTROLLER_PYGAME[player]["down"]]:
        acc = -100
    if keys[CONTROLLER_PYGAME[player]["act"]]:
        act = 1
    return (acc, dir, act)


def player_http(player: int, host: str, port: int) -> None:
    pygame_init()
    print(f"--- Start http player {player} ---")
    prev_acc = prev_dir = prev_act = 0
    clock = pygame.time.Clock()
    try:
        while True:
            acc, dir, act = control_player_pygame(player, clock)
            if acc == prev_acc and dir == prev_dir and act == prev_act:
                continue
            prev_acc = acc
            prev_dir = dir
            prev_act = act
            msg = f"{player},{acc},{dir},{act}"
            requests.post(f"http://{host}:{port}", data=msg)
    except KeyboardInterrupt:
        pass
    print(f"--- Stop http player {player} ---")


def player_tcp(player: int, host: str, port: int) -> None:
    pygame_init()
    print(f"--- Start TCP player {player} ---")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    prev_acc = prev_dir = prev_act = 0
    clock = pygame.time.Clock()
    try:
        while True:
            acc, dir, act = control_player_pygame(player, clock)
            if acc == prev_acc and dir == prev_dir and act == prev_act:
                continue
            prev_acc = acc
            prev_dir = dir
            prev_act = act
            msg = f"{player},{acc},{dir},{act},"
            if len(msg) < 32:
                msg += str(0) * (32 - len(msg))
            data = msg.encode("utf-8")
            s.sendall(data)
    except KeyboardInterrupt:
        pass
    s.close()
    print(f"--- Stop TCP player {player} ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", choices=["http", "tcp"], default="http")
    parser.add_argument("--player", choices=["1", "2", "3", "4"], default="1")
    parser.add_argument("--host", default=("10.77.2.39"))
    parser.add_argument("--port", default="8001")
    args = parser.parse_args()
    if args.protocol == "http":
        player_http(int(args.player), args.host, int(args.port))
    else:
        player_tcp(int(args.player), args.host, int(args.port))
