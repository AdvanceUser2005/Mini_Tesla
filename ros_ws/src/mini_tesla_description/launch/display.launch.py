"""View the 10C4I model in RViz with joint sliders (no simulation).

ros2 launch mini_tesla_description display.launch.py side_radars:=true
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg = get_package_share_directory("mini_tesla_description")
    xacro_file = os.path.join(pkg, "urdf", "mini_tesla.urdf.xacro")
    args = [DeclareLaunchArgument(n, default_value=d) for n, d in
            (("side_radars", "false"), ("rear_radar", "false"), ("laptop", "true"))]
    robot_description = ParameterValue(
        Command(["xacro ", xacro_file,
                 " side_radars:=", LaunchConfiguration("side_radars"),
                 " rear_radar:=", LaunchConfiguration("rear_radar"),
                 " laptop:=", LaunchConfiguration("laptop")]),
        value_type=str)
    return LaunchDescription(args + [
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             parameters=[{"robot_description": robot_description}]),
        Node(package="joint_state_publisher_gui", executable="joint_state_publisher_gui"),
        Node(package="rviz2", executable="rviz2",
             arguments=["-d", os.path.join(pkg, "config", "mini_tesla.rviz")]),
    ])
