import socket
from threading import Event, Thread
from typing import Callable


def create_keyboard_socket(port: int, stop: Event, process_command: Callable, cleanup: Callable) -> None:
    while not stop.is_set():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", port))
            s.listen()
            s.settimeout(1)
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue
            with conn:
                print("Connected by", addr)
                while not stop.is_set():
                    data = conn.recv(32)
                    if len(data) < 1:
                        break
                    process_command(data.decode())
            print(f"Disconnected", addr)
            cleanup()


def run_tcp_socket_server(port1: int, port2: int, process_command: Callable, cleanup: Callable) -> None:
    stop = Event()
    t_1 = Thread(target=create_keyboard_socket, args=(port1, stop, process_command, cleanup))
    t_2 = Thread(target=create_keyboard_socket, args=(port2, stop, process_command, cleanup))
    t_1.start()
    t_2.start()

    try:
        Event().wait()
    except KeyboardInterrupt:
        stop.set()

    t_1.join()
    t_2.join()

    cleanup()
    print("--- Exit TCP server ---")
