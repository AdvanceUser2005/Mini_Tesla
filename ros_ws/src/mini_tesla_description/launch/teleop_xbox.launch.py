"""Drive the 10C4I with an Xbox controller (publishes /cmd_vel).

ros2 launch mini_tesla_description teleop_xbox.launch.py
  use_sim_time:=true|false  (true when running with sim.launch.py)
Hold LB to drive; RT / LT raise / lower the speed limit. Left stick = forward/strafe, right stick X = turn.
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    cfg = os.path.join(get_package_share_directory("mini_tesla_description"), "config", "xbox_teleop.yaml")
    sim_time = ParameterValue(LaunchConfiguration("use_sim_time"), value_type=bool)
    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        Node(package="joy", executable="joy_node", parameters=[cfg, {"use_sim_time": sim_time}]),
        Node(package="mini_tesla_description", executable="xbox_teleop.py", name="xbox_teleop", output="screen",
             parameters=[cfg, {"use_sim_time": sim_time}]),
    ])
