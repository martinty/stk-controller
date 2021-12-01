# stk-controller

Remote keyboard controller for SuperTuxKart.

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

For TCP the msg need to be padded to 32 bytes before sending.

```sh
"player,acc,dir,act,padding"
```

## Dependencies

```sh
# For server (server.py)
python3 -m pip install pynput
```

```sh
# For pygame controller (player_x.py)
python3 -m pip install pygame
```
