
import math
import time

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class XboxDrive(Node):

    def __init__(self):
        super().__init__("xbox_drive")

        # ROS communication
        self.publisher = self.create_publisher(
            Twist, "/cmd_vel", 10
        )

        self.subscription = self.create_subscription(
            Joy, "/joy", self.joy_callback, 10
        )

        # Xbox controller mappings
        self.LEFT_X = 0
        self.LEFT_Y = 1
        self.RIGHT_X = 2

        self.B = 1
        self.Y = 3

        # Maximum commanded velocities
        self.max_speed = 0.15
        self.max_turn_rate = 0.50

        # Controller settings
        self.deadband = 0.10
        self.timeout = 0.35

        # Initial drive state
        self.enabled = False
        self.half_speed = True

        # Button edge detection
        self.last_y = False
        self.last_b = False

        # Joystick commands
        self.vx = 0.0
        self.vy = 0.0
        self.wz = 0.0

        self.last_joy = None

        # Publish at 20 Hz
        self.timer = self.create_timer(
            0.05, self.publish_velocity
        )

        self.get_logger().info(
            "Mini Tesla - Drive DISABLED - HALF SPEED"
        )

    def apply_deadband(self, value):

        if abs(value) < self.deadband:
            return 0.0

        return value

    def joy_callback(self, msg):

        if len(msg.axes) < 3 or len(msg.buttons) < 4:
            return

        axes = [
            float(msg.axes[self.LEFT_X]),
            float(msg.axes[self.LEFT_Y]),
            float(msg.axes[self.RIGHT_X])
        ]

        if not all(math.isfinite(x) for x in axes):
            return

        now = time.monotonic()

        y_pressed = msg.buttons[self.Y] == 1
        b_pressed = msg.buttons[self.B] == 1

        # First packet: initialize button states
        if self.last_joy is None:
            self.last_joy = now
            self.last_y = y_pressed
            self.last_b = b_pressed
            return

        # Communication interruption
        if now - self.last_joy > self.timeout:

            self.enabled = False
            self.vx = 0.0
            self.vy = 0.0
            self.wz = 0.0

            self.last_joy = now
            self.last_y = y_pressed
            self.last_b = b_pressed

            self.get_logger().warning(
                "Controller reconnected - Drive DISABLED"
            )
            return

        self.last_joy = now

        # Read joysticks
        left_x = self.apply_deadband(
            max(-1.0, min(1.0, axes[0]))
        )

        left_y = self.apply_deadband(
            max(-1.0, min(1.0, axes[1]))
        )

        right_x = self.apply_deadband(
            max(-1.0, min(1.0, axes[2]))
        )

        # Y button: drive toggle
        if y_pressed and not self.last_y:

            if self.enabled:

                self.enabled = False

                self.get_logger().info(
                    "Drive DISABLED"
                )

            elif (
                left_x == 0.0
                and left_y == 0.0
                and right_x == 0.0
            ):

                self.enabled = True

                self.get_logger().info(
                    "Drive ENABLED"
                )

            else:

                self.get_logger().warning(
                    "Center joysticks before enabling"
                )

        self.last_y = y_pressed

        # B button: speed mode toggle
        if b_pressed and not self.last_b:

            self.half_speed = not self.half_speed

            if self.half_speed:
                self.get_logger().info(
                    "HALF SPEED"
                )
            else:
                self.get_logger().info(
                    "FULL SPEED"
                )

        self.last_b = b_pressed

        # Mecanum body-frame movement commands
        self.vx = -left_y
        self.vy = -left_x
        self.wz = -right_x

        # Normalize diagonal translation
        magnitude = math.hypot(self.vx, self.vy)

        if magnitude > 1.0:
            self.vx /= magnitude
            self.vy /= magnitude

    def publish_velocity(self):

        cmd = Twist()

        now = time.monotonic()

        # Communication watchdog
        if (
            self.last_joy is None
            or now - self.last_joy > self.timeout
        ):

            if self.enabled:
                self.get_logger().warning(
                    "Controller timeout - Drive DISABLED"
                )

            self.enabled = False

        if self.enabled:

            speed_factor = (
                0.5 if self.half_speed else 1.0
            )

            cmd.linear.x = (
                self.vx * self.max_speed * speed_factor
            )

            cmd.linear.y = (
                self.vy * self.max_speed * speed_factor
            )

            cmd.angular.z = (
                self.wz * self.max_turn_rate * speed_factor
            )

        # Otherwise all velocities remain zero
        self.publisher.publish(cmd)


def main():

    rclpy.init()

    node = XboxDrive()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.publisher.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
