"""Gazebo Harmonic simulation of the Mini Tesla 10C4I.

ros2 launch mini_tesla_description sim.launch.py
  drive:=mecanum|planar  side_radars:=false|true  rear_radar:=false|true  laptop:=true|false
  world:=<path to .sdf>  rviz:=true|false  x:= y:= yaw:=  (spawn pose)
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg = get_package_share_directory("mini_tesla_description")
    xacro_file = os.path.join(pkg, "urdf", "mini_tesla.urdf.xacro")

    args = [
        DeclareLaunchArgument("drive", default_value="mecanum", description="mecanum | planar"),
        DeclareLaunchArgument("side_radars", default_value="false"),
        DeclareLaunchArgument("rear_radar", default_value="false"),
        DeclareLaunchArgument("laptop", default_value="true"),
        DeclareLaunchArgument("world", default_value=os.path.join(pkg, "worlds", "test_arena.sdf")),
        DeclareLaunchArgument("rviz", default_value="true"),
        DeclareLaunchArgument("x", default_value="0.0"),
        DeclareLaunchArgument("y", default_value="0.0"),
        DeclareLaunchArgument("yaw", default_value="0.0"),
    ]

    robot_description = ParameterValue(
        Command(["xacro ", xacro_file,
                 " drive:=", LaunchConfiguration("drive"),
                 " side_radars:=", LaunchConfiguration("side_radars"),
                 " rear_radar:=", LaunchConfiguration("rear_radar"),
                 " laptop:=", LaunchConfiguration("laptop")]),
        value_type=str)

    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")),
        launch_arguments={"gz_args": ["-r -v 3 ", LaunchConfiguration("world")],
                          "on_exit_shutdown": "true"}.items())

    rsp = Node(package="robot_state_publisher", executable="robot_state_publisher",
               parameters=[{"robot_description": robot_description, "use_sim_time": True}],
               output="screen")

    spawn = Node(package="ros_gz_sim", executable="create", output="screen",
                 arguments=["-topic", "robot_description", "-name", "mini_tesla",
                            "-x", LaunchConfiguration("x"), "-y", LaunchConfiguration("y"),
                            "-z", "0.01", "-Y", LaunchConfiguration("yaw")])

    bridge = Node(package="ros_gz_bridge", executable="parameter_bridge", output="screen",
                  parameters=[{"config_file": os.path.join(pkg, "config", "bridge.yaml"),
                               "use_sim_time": True}])

    tof = Node(package="mini_tesla_description", executable="tof_to_range.py",
               parameters=[{"use_sim_time": True}], output="screen")

    rviz = Node(package="rviz2", executable="rviz2", condition=IfCondition(LaunchConfiguration("rviz")),
                arguments=["-d", os.path.join(pkg, "config", "mini_tesla.rviz")],
                parameters=[{"use_sim_time": True}])

    return LaunchDescription(args + [gz, rsp, spawn, bridge, tof, rviz])
