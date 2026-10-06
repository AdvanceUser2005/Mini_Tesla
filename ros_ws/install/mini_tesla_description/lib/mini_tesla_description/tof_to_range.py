#!/usr/bin/env python3
"""Turn each simulated VL53L1X fan (LaserScan) into the single distance the real sensor reports.

Subscribes  /tof/<name>/scan   (sensor_msgs/LaserScan, from Gazebo)
Publishes   /tof/<name>/range  (sensor_msgs/Range, INFRARED, 27 deg FoV, 0.04-4.0 m)
Range = nearest valid beam; out of range -> +inf (REP-117).
"""
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan, Range

TOFS = ["front_left", "front_right", "rear_left", "rear_right",
        "left_front", "left_rear", "right_front", "right_rear"]


class TofToRange(Node):
    def __init__(self):
        super().__init__("tof_to_range")
        self.declare_parameter("field_of_view", math.radians(27.0))
        self.fov = self.get_parameter("field_of_view").value
        self.pubs = {}
        for name in TOFS:
            self.pubs[name] = self.create_publisher(Range, f"/tof/{name}/range", qos_profile_sensor_data)
            self.create_subscription(LaserScan, f"/tof/{name}/scan",
                                     lambda msg, n=name: self.on_scan(n, msg), qos_profile_sensor_data)

    def on_scan(self, name, scan):
        valid = [r for r in scan.ranges if math.isfinite(r) and scan.range_min <= r <= scan.range_max]
        out = Range()
        out.header = scan.header
        out.radiation_type = Range.INFRARED
        out.field_of_view = float(self.fov)
        out.min_range = scan.range_min
        out.max_range = scan.range_max
        out.range = min(valid) if valid else math.inf
        self.pubs[name].publish(out)


def main():
    rclpy.init()
    node = TofToRange()
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
