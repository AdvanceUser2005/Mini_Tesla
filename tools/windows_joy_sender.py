"""Run on WINDOWS: read the Xbox controller and stream it to ROS in WSL / Docker (scripts/tcp_joy.py).

WSL2's kernel has no joystick drivers, so the controller stays on the Windows side and is sent over TCP instead.

    pip install pygame
    python windows_joy_sender.py                 # connects to localhost:9870 (WSL forwards it)
    python windows_joy_sender.py 172.23.14.119   # or the WSL IP if localhost forwarding is off

Sends one line per tick, already in the Linux joy_node layout that config/xbox_teleop.yaml expects:
    axes    0 LX (left +)  1 LY (up +)  2 LT (+1 released, -1 pressed)  3 RX (left +)  4 RY (up +)  5 RT
    buttons 0 A  1 B  2 X  3 Y  4 LB  5 RB  6 Back  7 Start  8 Guide  9 LS  10 RS
"""
import socket
import sys
import time

import pygame
from pygame._sdl2 import controller

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 9870
RATE = 50.0
DEADZONE = 0.1

BUTTONS = [pygame.CONTROLLER_BUTTON_A, pygame.CONTROLLER_BUTTON_B, pygame.CONTROLLER_BUTTON_X,
           pygame.CONTROLLER_BUTTON_Y, pygame.CONTROLLER_BUTTON_LEFTSHOULDER, pygame.CONTROLLER_BUTTON_RIGHTSHOULDER,
           pygame.CONTROLLER_BUTTON_BACK, pygame.CONTROLLER_BUTTON_START, pygame.CONTROLLER_BUTTON_GUIDE,
           pygame.CONTROLLER_BUTTON_LEFTSTICK, pygame.CONTROLLER_BUTTON_RIGHTSTICK]


def stick(pad, axis, sign):
    v = sign * pad.get_axis(axis) / 32767.0
    return 0.0 if abs(v) < DEADZONE else max(-1.0, min(1.0, v))


def trigger(pad, axis):
    return 1.0 - 2.0 * pad.get_axis(axis) / 32767.0     # SDL 0..32767 -> joy_node +1..-1


def open_pad():
    controller.init()
    while True:
        pygame.event.pump()
        for i in range(controller.get_count()):
            if controller.is_controller(i):
                pad = controller.Controller(i)
                print(f"controller: {pad.name}")
                return pad
        print("no controller found, retrying...")
        time.sleep(1.0)


def main():
    pygame.init()
    pad = open_pad()
    while True:
        try:
            sock = socket.create_connection((HOST, PORT), timeout=2.0)
        except OSError as e:
            print(f"cannot reach {HOST}:{PORT} ({e}); is tcp_joy running? retrying...")
            time.sleep(1.0)
            continue
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        print(f"streaming to {HOST}:{PORT}  (Ctrl+C to quit)")
        try:
            while True:
                pygame.event.pump()
                if not pad.attached():
                    print("controller disconnected")
                    pad = open_pad()
                axes = [stick(pad, pygame.CONTROLLER_AXIS_LEFTX, -1), stick(pad, pygame.CONTROLLER_AXIS_LEFTY, -1),
                        trigger(pad, pygame.CONTROLLER_AXIS_TRIGGERLEFT),
                        stick(pad, pygame.CONTROLLER_AXIS_RIGHTX, -1), stick(pad, pygame.CONTROLLER_AXIS_RIGHTY, -1),
                        trigger(pad, pygame.CONTROLLER_AXIS_TRIGGERRIGHT)]
                buttons = [int(pad.get_button(b)) for b in BUTTONS]
                line = " ".join(f"{a:.3f}" for a in axes) + " | " + " ".join(map(str, buttons)) + "\n"
                sock.sendall(line.encode())
                time.sleep(1.0 / RATE)
        except OSError:
            print("connection lost, reconnecting...")
            sock.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
