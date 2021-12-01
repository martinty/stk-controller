# pygame http or TCP client controller
# python -m pip install pygame
# python -m pip install requests

import argparse
import socket
from typing import Tuple

import pygame
import requests

CONTROLLER = {
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


def control_player(player: int) -> Tuple[int, int, int]:
    acc = dir = act = 0
    keys = pygame.key.get_pressed()
    if keys[CONTROLLER[player]["left"]]:
        dir = -100
    elif keys[CONTROLLER[player]["right"]]:
        dir = 100
    if keys[CONTROLLER[player]["up"]]:
        acc = 100
    elif keys[CONTROLLER[player]["down"]]:
        acc = -100
    if keys[CONTROLLER[player]["act"]]:
        act = 1
    return (acc, dir, act)


def player_http(player: int, host: str, port: int) -> None:
    pygame_init()
    prev_acc = prev_dir = prev_act = 0
    clock = pygame.time.Clock()
    try:
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.name(event.key))
            acc, dir, act = control_player(player)
            if acc == prev_acc and dir == prev_dir and act == prev_act:
                continue
            prev_acc = acc
            prev_dir = dir
            prev_act = act
            msg = f"{player},{acc},{dir},{act}"
            requests.post(f"http://{host}:{port}", data=msg)
    except KeyboardInterrupt:
        pass


def player_tcp(player: int, host: str, port: int) -> None:
    pygame_init()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    prev_acc = prev_dir = prev_act = 0
    clock = pygame.time.Clock()
    try:
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.name(event.key))
            acc, dir, act = control_player(player)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", choices=["http", "tcp"], default="http")
    parser.add_argument("--player", choices=[1, 2, 3, 4], default=1)
    parser.add_argument("--host", default=("10.77.2.39"))
    parser.add_argument("--port", default=8001)
    args = parser.parse_args()
    if args.protocol == "http":
        player_http(args.player, args.host, args.port)
    else:
        player_tcp(args.player, args.host, args.port)
