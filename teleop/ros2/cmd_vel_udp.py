
import json
import math
import socket
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocitySender(Node):

    def __init__(self):
        super().__init__("velocity_sender")

        # Windows host and UDP port
        self.host = "host.docker.internal"
        self.port = 5006

        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        # Subscribe to ROS velocity commands
        self.subscription = self.create_subscription(
            Twist,
            "/cmd_vel",
            self.velocity_callback,
            10
        )

        # Safety timeout and command state
        self.timeout = 0.35
        self.last_command = None

        self.vx = 0.0
        self.vy = 0.0
        self.wz = 0.0

        # Send data at 20 Hz
        self.timer = self.create_timer(
            0.05,
            self.send_velocity
        )

        self.get_logger().info(
            "ROS velocity sender started"
        )

    def velocity_callback(self, msg):

        values = [
            msg.linear.x,
            msg.linear.y,
            msg.angular.z
        ]

        if not all(math.isfinite(v) for v in values):
            return

        self.vx = float(msg.linear.x)
        self.vy = float(msg.linear.y)
        self.wz = float(msg.angular.z)

        self.last_command = time.monotonic()

    def send_velocity(self):

        # If ROS commands stop, send zero velocity
        if (
            self.last_command is None
            or time.monotonic() - self.last_command > self.timeout
        ):
            vx = 0.0
            vy = 0.0
            wz = 0.0

        else:
            vx = self.vx
            vy = self.vy
            wz = self.wz

        data = {
            "vx": vx,
            "vy": vy,
            "wz": wz
        }

        message = json.dumps(data).encode("utf-8")

        self.sock.sendto(
            message,
            (self.host, self.port)
        )

    def close(self):
        self.sock.close()


def main():

    rclpy.init()
    node = VelocitySender()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
