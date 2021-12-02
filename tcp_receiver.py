import socket
from threading import Event, Thread
from typing import Callable, List, Tuple


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
                print(f"Connected by addr={addr}, port={port}")
                while not stop.is_set():
                    data = conn.recv(32)  # Will block until client send new msg or close connection.
                    if len(data) < 1:
                        break
                    process_command(data.decode())
            print(f"Disconnected addr={addr}, port={port}")


def run_tcp_socket_server(ports: Tuple, process_command: Callable, cleanup: Callable) -> None:
    print("--- Starting TCP server ---")
    stop = Event()
    threads: List[Thread] = []
    for port in ports:
        threads.append(Thread(target=create_keyboard_socket, args=(port, stop, process_command, cleanup)))
    for t in threads:
        t.start()

    try:
        Event().wait()
    except KeyboardInterrupt:
        stop.set()

    for t in threads:
        t.join()

    cleanup()
    print("--- Stopping TCP server ---")
