# stk-controller

Remote keyboard controller for SuperTuxKart. The SuperTuxKart window has to be in focus when the server is running.

## Client

Should only send msg to the server if the kart's state change.

## States

```sh
player: [1, 2, 3, 4]
acc: [-1, 0, 1]
dir: [-1, 0, 1]
act: [0, 1]
```

## Msg format

```sh
"player,acc,dir,act"
```

## Note

For TCP and UDP the msg need to be padded to 32 bytes before sending.

```sh
"player,acc,dir,act,padding"
```

For `pygame` controller to work the `pygame` window has the be in focus to register keystrokes.

## Dependencies

```sh
# For server (server.py)
python3 -m pip install pynput
```

```sh
# For pygame controller (player.py)
python3 -m pip install pygame
python3 -m pip install requests  # http only
```
