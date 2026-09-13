from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    package_name = 'tesla_description'

    xacro_file = os.path.join(
        get_package_share_directory(package_name),
        'urdf',
        'robot.urdf.xacro'
    )

    robot_description = Command([
        'xacro ',
        xacro_file
    ])

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description}
        ]
    )

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    return LaunchDescription([
        joint_state_publisher_gui,
        robot_state_publisher
    ])