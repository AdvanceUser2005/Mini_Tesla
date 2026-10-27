#!/usr/bin/env python3
"""TCP -> /joy, for a controller plugged into Windows while ROS runs in WSL2 / Docker (no joystick drivers there).

Listens on 0.0.0.0:`port` for tools/windows_joy_sender.py, which sends lines of "<axes...> | <buttons...>" already in
joy_node's Linux layout. Publishes /joy (sensor_msgs/Joy) for every line received; when the sender stops, /joy stops
and xbox_teleop.py's joy_timeout halts the robot.
"""
import socket
import threading

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy


class TcpJoy(Node):
    def __init__(self):
        super().__init__("tcp_joy")
        self.declare_parameter("port", 9870)
        self.port = self.get_parameter("port").value
        self.pub = self.create_publisher(Joy, "/joy", 10)
        threading.Thread(target=self.serve, daemon=True).start()

    def serve(self):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("0.0.0.0", self.port))
        srv.listen(1)
        self.get_logger().info(f"waiting for windows_joy_sender.py on port {self.port}")
        while rclpy.ok():
            conn, addr = srv.accept()
            conn.settimeout(1.0)
            self.get_logger().info(f"controller connected from {addr[0]}")
            buf = b""
            try:
                while rclpy.ok():
                    data = conn.recv(4096)
                    if not data:
                        break
                    buf += data
                    *lines, buf = buf.split(b"\n")
                    for line in lines:
                        self.publish(line.decode(errors="replace"))
            except (OSError, socket.timeout):
                pass
            conn.close()
            self.get_logger().warn("controller disconnected")

    def publish(self, line):
        try:
            axes, buttons = line.split("|")
            msg = Joy()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.axes = [float(a) for a in axes.split()]
            msg.buttons = [int(b) for b in buttons.split()]
        except ValueError:
            return
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = TcpJoy()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
