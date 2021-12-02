# Server with HTTP or TCP
# python3 -m pip install pynput

import argparse

from pynput.keyboard import Controller, Key

from http_receiver import run_http_server
from tcp_receiver import run_tcp_socket_server
from udp_receiver import run_udp_socket_server


PORTS_TCP = (8001, 8002, 8003, 8004)
PORT_HTTP = 8005
PORT_UDP = 8006

CONTROLLER = {
    1: {
        "up": Key.up,
        "down": Key.down,
        "right": Key.right,
        "left": Key.left,
        "act": Key.space,
    },
    2: {
        "up": "w",
        "down": "s",
        "right": "d",
        "left": "a",
        "act": "f",
    },
    3: {
        "up": "4",
        "down": "r",
        "right": "t",
        "left": "e",
        "act": "y",
    },
    4: {
        "up": "u",
        "down": "j",
        "right": "k",
        "left": "h",
        "act": "l",
    },
}


def control_player(keyboard, player: int, acc: int, dir: int, act: int) -> None:
    # Acceleration
    if acc < 0:
        keyboard.release(CONTROLLER[player]["up"])
        keyboard.press(CONTROLLER[player]["down"])
    elif acc > 0:
        keyboard.release(CONTROLLER[player]["down"])
        keyboard.press(CONTROLLER[player]["up"])
    else:
        keyboard.release(CONTROLLER[player]["up"])
        keyboard.release(CONTROLLER[player]["down"])

    # Direction
    if dir < 0:
        keyboard.release(CONTROLLER[player]["right"])
        keyboard.press(CONTROLLER[player]["left"])
    elif dir > 0:
        keyboard.release(CONTROLLER[player]["left"])
        keyboard.press(CONTROLLER[player]["right"])
    else:
        keyboard.release(CONTROLLER[player]["right"])
        keyboard.release(CONTROLLER[player]["left"])

    # Action (fire)
    if act:
        keyboard.press(CONTROLLER[player]["act"])
    else:
        keyboard.release(CONTROLLER[player]["act"])


def release_all_keys(keyboard) -> None:
    for keys in CONTROLLER.values():
        for k in keys.values():
            keyboard.release(k)


def main(protocol) -> None:
    keyboard = Controller()

    def process_command(data: str) -> None:
        player_input = data.split(",")
        player = int(player_input[0])
        acc = int(player_input[1])
        dir = int(player_input[2])
        act = int(player_input[3])
        control_player(keyboard, player, acc, dir, act)

    def cleanup() -> None:
        release_all_keys(keyboard)

    if protocol == "http":
        run_http_server(PORT_HTTP, process_command, cleanup)
    elif protocol == "tcp":
        run_tcp_socket_server(PORTS_TCP, process_command, cleanup)
    else:
        run_udp_socket_server(PORT_UDP, process_command, cleanup)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", choices=["http", "tcp", "udp"], default="http")
    args = parser.parse_args()
    main(args.protocol)
