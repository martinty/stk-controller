# Server with TCP
# python3 -m pip install pynput
import multiprocessing as mp
import socket

from pynput.keyboard import Controller, Key


HOST = "0.0.0.0"
PORT_1 = 8001
PORT_2 = 8002
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


def server_tcp(host, port) -> None:
    keyboard = Controller()
    try:
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((host, port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print("Connected by", addr)
                    while True:
                        data = conn.recv(32)
                        if len(data) < 1:
                            break
                        player_input = data.decode().split(",")
                        player = int(player_input[0])
                        acc = int(player_input[1])
                        dir = int(player_input[2])
                        act = int(player_input[3])
                        control_player(keyboard, player, acc, dir, act)
                print(f"Disconnected", addr)
                release_all_keys(keyboard)
    except KeyboardInterrupt:
        release_all_keys(keyboard)


def main() -> None:
    p_1 = mp.Process(target=server_tcp, args=(HOST, PORT_1))
    p_2 = mp.Process(target=server_tcp, args=(HOST, PORT_2))
    p_1.start()
    p_2.start()

    try:
        mp.Event().wait()
    except KeyboardInterrupt:
        pass

    p_1.join()
    p_2.join()

    print("--- Exit Server ---")


if __name__ == "__main__":
    main()
