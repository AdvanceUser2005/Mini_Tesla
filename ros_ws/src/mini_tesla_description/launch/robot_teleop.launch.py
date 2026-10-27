"""Drive the real 10C4I with an Xbox controller: joy + xbox_teleop.py -> /cmd_vel -> teensy_bridge.py -> Teensy.

ros2 launch mini_tesla_description robot_teleop.launch.py
  port:=/dev/ttyACM0  (Teensy USB serial)   pwm_limit:=160  (0-255, cap on any wheel)
  joy_source:=device|tcp  (tcp: controller on Windows via tools/windows_joy_sender.py)
Hold LB to drive; RT / LT raise / lower the speed limit. Left stick = forward/strafe, right stick X = turn.
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg = get_package_share_directory("mini_tesla_description")
    teleop = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg, "launch", "teleop_xbox.launch.py")),
        launch_arguments={"use_sim_time": "false"}.items())
    bridge = Node(package="mini_tesla_description", executable="teensy_bridge.py", name="teensy_bridge",
                  output="screen",
                  parameters=[{"port": LaunchConfiguration("port"),
                               "pwm_limit": ParameterValue(LaunchConfiguration("pwm_limit"), value_type=int)}])
    return LaunchDescription([
        DeclareLaunchArgument("port", default_value="/dev/ttyACM0"),
        DeclareLaunchArgument("pwm_limit", default_value="160"),
        teleop,
        bridge,
    ])
