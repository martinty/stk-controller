import socket
import multiprocessing as mp


def create_keyboard_socket(port, process_command, cleanup) -> None:
    try:
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("0.0.0.0", port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print("Connected by", addr)
                    while True:
                        data = conn.recv(32)
                        if len(data) < 1:
                            break

                        process_command(data.decode())
                print(f"Disconnected", addr)
                cleanup()
    except KeyboardInterrupt:
        cleanup()


def run_tcp_socket_server(port1, port2, process_command, cleanup):
    p_1 = mp.Process(target=create_keyboard_socket, args=(port1, process_command, cleanup))
    p_2 = mp.Process(target=create_keyboard_socket, args=(port2, process_command, cleanup))
    p_1.start()
    p_2.start()

    try:
        mp.Event().wait()
    except KeyboardInterrupt:
        pass

    p_1.join()
    p_2.join()

    print("--- Exit Server ---")
