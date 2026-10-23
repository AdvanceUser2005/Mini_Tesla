#!/usr/bin/env python3
"""Xbox controller -> /cmd_vel for the holonomic 10C4I, with trigger-controlled speed.

Subscribes  /joy      (sensor_msgs/Joy)
Publishes   /cmd_vel  (geometry_msgs/Twist, 20 Hz while driving)

Left stick = forward / strafe, right stick X = turn. Hold LB to drive (dead-man switch).
RT raises the speed limit and LT lowers it, for as long as the trigger is held (the harder you press,
the faster it changes). The limit is a fraction of max_linear / max_angular and is kept between presses.
"""
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Joy


class XboxTeleop(Node):
    def __init__(self):
        super().__init__("xbox_teleop")
        for name, default in (
                ("axis_forward", 1), ("axis_strafe", 0), ("axis_yaw", 3),
                ("axis_lt", 2), ("axis_rt", 5), ("enable_button", 4),
                ("max_linear", 1.2), ("max_angular", 2.5),
                ("min_speed", 0.1), ("initial_speed", 0.4),
                ("speed_rate", 0.5),        # speed fraction per second at full trigger
                ("joy_timeout", 0.5), ("rate", 20.0)):
            self.declare_parameter(name, default)
        self.p = {n: self.get_parameter(n).value for n in (
            "axis_forward", "axis_strafe", "axis_yaw", "axis_lt", "axis_rt", "enable_button",
            "max_linear", "max_angular", "min_speed", "initial_speed", "speed_rate", "joy_timeout", "rate")}
        self.speed = self.p["initial_speed"]
        self.joy = None
        self.last_joy = self.get_clock().now()
        self.seen = set()       # trigger axes that have reported a real value (they read 0.0 until first touched)
        self.was_driving = False
        self.last_logged = None
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.create_subscription(Joy, "/joy", self.on_joy, 10)
        self.create_timer(1.0 / self.p["rate"], self.tick)

    def on_joy(self, msg):
        self.joy = msg
        self.last_joy = self.get_clock().now()

    def axis(self, i):
        return self.joy.axes[i] if i < len(self.joy.axes) else 0.0

    def trigger(self, i):
        """0 (released) .. 1 (fully pressed). Triggers rest at +1 and go to -1 when pressed."""
        v = self.axis(i)
        if v != 0.0:
            self.seen.add(i)
        return (1.0 - v) / 2.0 if i in self.seen else 0.0

    def tick(self):
        stale = (self.get_clock().now() - self.last_joy).nanoseconds * 1e-9 > self.p["joy_timeout"]
        enabled = (self.joy is not None and not stale and
                   self.p["enable_button"] < len(self.joy.buttons) and
                   self.joy.buttons[self.p["enable_button"]])
        if not enabled:
            if self.was_driving:
                self.pub.publish(Twist())
                self.was_driving = False
            return
        self.was_driving = True

        dt = 1.0 / self.p["rate"]
        dv = (self.trigger(self.p["axis_rt"]) - self.trigger(self.p["axis_lt"])) * self.p["speed_rate"] * dt
        self.speed = min(1.0, max(self.p["min_speed"], self.speed + dv))
        if self.last_logged is None or abs(self.speed - self.last_logged) >= 0.05:
            self.last_logged = self.speed
            self.get_logger().info(f"speed {self.speed * 100:.0f}% "
                                   f"({self.speed * self.p['max_linear']:.2f} m/s, "
                                   f"{self.speed * self.p['max_angular']:.2f} rad/s)")

        cmd = Twist()
        cmd.linear.x = self.axis(self.p["axis_forward"]) * self.speed * self.p["max_linear"]
        cmd.linear.y = self.axis(self.p["axis_strafe"]) * self.speed * self.p["max_linear"]
        cmd.angular.z = self.axis(self.p["axis_yaw"]) * self.speed * self.p["max_angular"]
        self.pub.publish(cmd)


def main():
    rclpy.init()
    node = XboxTeleop()
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
