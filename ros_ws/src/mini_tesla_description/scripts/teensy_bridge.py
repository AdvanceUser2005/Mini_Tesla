#!/usr/bin/env python3
"""/cmd_vel -> Teensy 4.1 motor PWM over USB serial (real robot, open loop).

Subscribes  /cmd_vel  (geometry_msgs/Twist: linear.x, linear.y, angular.z)
Sends       "M <fl> <rl> <fr> <rr>\\n" at `rate` Hz, each -255..255 (Mini_Tesla_Firmware/src/main.cpp)

Mecanum X kinematics, same signs as the firmware's tested W/A/Q keys. Wheel speed (m/s) is mapped linearly to PWM
with max_wheel_speed = PWM 255, then all four are scaled down together if any exceeds pwm_limit, so the direction of
travel is kept. If /cmd_vel goes quiet for cmd_timeout the bridge sends zeros; the firmware also stops by itself
if the bridge dies (250 ms watchdog).
"""
import rclpy
import serial
from geometry_msgs.msg import Twist
from rclpy.node import Node


class TeensyBridge(Node):
    def __init__(self):
        super().__init__("teensy_bridge")
        for name, default in (
                ("port", "/dev/ttyACM0"), ("baud", 115200),
                ("wheel_x", 0.13305), ("wheel_y", 0.1344),   # axle half-wheelbase / half-track, from the URDF
                ("max_wheel_speed", 2.0),   # m/s of wheel rim at PWM 255 (19:1 37D, 12 V, 75 mm wheel ~ 2.08 no-load)
                ("pwm_limit", 160),         # hard cap on |PWM| sent to any wheel
                ("cmd_timeout", 0.3), ("rate", 30.0)):
            self.declare_parameter(name, default)
        self.p = {n: self.get_parameter(n).value for n in (
            "port", "baud", "wheel_x", "wheel_y", "max_wheel_speed", "pwm_limit", "cmd_timeout", "rate")}
        self.ser = serial.Serial(self.p["port"], self.p["baud"], timeout=0)
        self.get_logger().info(f"connected to Teensy on {self.p['port']}")
        self.cmd = Twist()
        self.last_cmd = None
        self.last_sent = None
        self.create_subscription(Twist, "/cmd_vel", self.on_cmd, 10)
        self.create_timer(1.0 / self.p["rate"], self.tick)

    def on_cmd(self, msg):
        self.cmd = msg
        self.last_cmd = self.get_clock().now()

    def wheel_pwm(self, vx, vy, wz):
        k = self.p["wheel_x"] + self.p["wheel_y"]
        speeds = (vx - vy - k * wz,     # FL
                  vx + vy - k * wz,     # RL
                  vx + vy + k * wz,     # FR
                  vx - vy + k * wz)     # RR
        pwm = [v / self.p["max_wheel_speed"] * 255.0 for v in speeds]
        peak = max(abs(v) for v in pwm)
        if peak > self.p["pwm_limit"]:
            pwm = [v * self.p["pwm_limit"] / peak for v in pwm]
        return [int(round(v)) for v in pwm]

    def tick(self):
        stale = (self.last_cmd is None or
                 (self.get_clock().now() - self.last_cmd).nanoseconds * 1e-9 > self.p["cmd_timeout"])
        pwm = [0, 0, 0, 0] if stale else self.wheel_pwm(self.cmd.linear.x, self.cmd.linear.y, self.cmd.angular.z)
        self.ser.write(("M %d %d %d %d\n" % tuple(pwm)).encode())
        if pwm != self.last_sent:
            self.last_sent = pwm
            self.get_logger().debug(f"pwm FL {pwm[0]} RL {pwm[1]} FR {pwm[2]} RR {pwm[3]}")
        for line in self.ser.read(self.ser.in_waiting or 0).decode(errors="replace").splitlines():
            if line.strip():
                self.get_logger().info(f"teensy: {line.strip()}")

    def stop(self):
        self.ser.write(b"M 0 0 0 0\n")
        self.ser.flush()
        self.ser.close()


def main():
    rclpy.init()
    node = TeensyBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
