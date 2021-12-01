import socket
import pygame

HOST = "10.77.2.39"  # IP server
PORT = 8004  # Port player 2


pygame.init()
pygame.display.set_mode(size=(400, 200))
clock = pygame.time.Clock()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    prev_acc = 0
    prev_dir = 0
    prev_act = 0
    try:
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.name(event.key))
            acc = 0
            dir = 0
            act = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_h]:
                dir = -100
            elif keys[pygame.K_k]:
                dir = 100
            if keys[pygame.K_u]:
                acc = 100
            elif keys[pygame.K_j]:
                acc = -100
            if keys[pygame.K_l]:
                act = 1
            if acc == prev_acc and dir == prev_dir and act == prev_act:
                continue
            prev_acc = acc
            prev_dir = dir
            prev_act = act
            msg = f"{4},{acc},{dir},{act},"
            if len(msg) < 32:
                msg += str(0) * (32 - len(msg))
            data = msg.encode("utf-8")
            s.sendall(data)
    except KeyboardInterrupt:
        pass

print("--- Exit Player 4 ---")
