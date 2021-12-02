import socket
from typing import Callable


def run_udp_socket_server(port: str, process_command: Callable, cleanup: Callable) -> None:
    print("--- Starting UDP server ---")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    try:
        while True:
            data = s.recv(32)
            process_command(data.decode())
    except KeyboardInterrupt:
        cleanup()
    print("--- Stopping UDP server ---")
