
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

import socket
import json
import time


class XboxReceiver(Node):

    def __init__(self):
        super().__init__("xbox_receiver")

        self.publisher = self.create_publisher(
            Joy, "/joy", 10
        )

        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM
        )

        self.sock.bind(("0.0.0.0", 5005))
        self.sock.settimeout(0.1)

        self.last_packet = time.monotonic()
        self.axes_count = 0
        self.buttons_count = 0
        self.connected = False

        self.get_logger().info(
            "Waiting for Xbox controller on UDP 5005..."
        )

    def run(self):

        while rclpy.ok():

            try:
                data, address = self.sock.recvfrom(4096)

                message = json.loads(
                    data.decode("utf-8")
                )

                axes = [float(x) for x in message["axes"]]
                buttons = [int(x) for x in message["buttons"]]

                joy = Joy()
                joy.header.stamp = self.get_clock().now().to_msg()
                joy.axes = axes
                joy.buttons = buttons

                self.publisher.publish(joy)

                self.last_packet = time.monotonic()
                self.axes_count = len(axes)
                self.buttons_count = len(buttons)

                if not self.connected:
                    self.get_logger().info(
                        "Xbox controller connected!"
                    )
                    self.connected = True

            except socket.timeout:

                if (
                    self.connected
                    and time.monotonic() - self.last_packet > 0.3
                ):

                    joy = Joy()
                    joy.header.stamp = self.get_clock().now().to_msg()
                    joy.axes = [0.0] * self.axes_count
                    joy.buttons = [0] * self.buttons_count

                    self.publisher.publish(joy)

                    self.get_logger().warning(
                        "Controller connection lost"
                    )
                    self.connected = False

            except (ValueError, KeyError, TypeError) as error:
                self.get_logger().warning(
                    f"Invalid controller packet: {error}"
                )


def main():

    rclpy.init()
    node = XboxReceiver()

    try:
        node.run()

    except KeyboardInterrupt:
        pass

    finally:
        node.sock.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
