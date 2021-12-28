# from launch import LaunchDescription, Command
# from launch_ros.actions import Node

import launch
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
import launch_ros
import os

def generate_launch_description():
    default_model_path = '/home/ubuntu/ws_mini/src/urdf/mini_bot.urdf' 

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        Node(
            package='diff_motor',
            executable='diff_velocity',
            namespace='mini_rover',
        ),
        Node(
            package='diff_motor',
            executable='diff_wheels',
            namespace='mini_rover',
        ),
        Node(
            package='diff_motor',
            executable='diff_odom',
            namespace='mini_rover',
        ),
        Node(
            package='diff_motor',
            executable='diff_motion',
            namespace='mini_rover',
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
        ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
        ),
        Node(
            package='rplidar_ros',
            executable='rplidar_composition',
            output='screen',
            namespace='mini_rover',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'serial_baudrate': 115200,  # A1 / A2
                # 'serial_baudrate': 256000, # A3
                'frame_id': 'laser',
                'inverted': False,
                'angle_compensate': True,
            }],
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=['/home/ubuntu/ws_mini/config/ekf.yaml']
        ),
    ])
