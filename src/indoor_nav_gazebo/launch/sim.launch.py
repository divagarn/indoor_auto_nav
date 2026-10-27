import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    gz_share = get_package_share_directory('gazebo_ros')
    desc_share = get_package_share_directory('indoor_nav_description')
    sim_share = get_package_share_directory('indoor_nav_gazebo')

    world = LaunchConfiguration('world')
    gui = LaunchConfiguration('gui')
    rviz = LaunchConfiguration('rviz')

    return LaunchDescription([
        DeclareLaunchArgument('world', default_value=os.path.join(sim_share, 'worlds', 'indoor_house.world')),
        DeclareLaunchArgument('gui', default_value='true', description='Show Gazebo client'),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('robot', default_value='nomad', description='pebble | nomad | sentinel'),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('yaw', default_value='0.0'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(gz_share, 'launch', 'gazebo.launch.py')),
            launch_arguments={'world': world, 'gui': gui, 'verbose': 'false'}.items()),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(desc_share, 'launch', 'rsp.launch.py')),
            launch_arguments={'use_sim_time': 'true', 'robot': LaunchConfiguration('robot')}.items()),

        Node(package='gazebo_ros', executable='spawn_entity.py', output='screen',
             arguments=['-topic', 'robot_description', '-entity', LaunchConfiguration('robot'),
                        '-x', LaunchConfiguration('x'), '-y', LaunchConfiguration('y'),
                        '-z', '0.01', '-Y', LaunchConfiguration('yaw')]),

        Node(package='rviz2', executable='rviz2', condition=IfCondition(rviz),
             arguments=['-d', os.path.join(desc_share, 'rviz', 'sim.rviz')],
             parameters=[{'use_sim_time': True}]),
    ])
