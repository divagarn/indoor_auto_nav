import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

import xacro

# Same round base, different heights.  mast_h = lidar mast above chassis top, cam_h = camera height
# above base_link origin (m).  Lidar height above ground ~ 0.075 + chassis_h/2 + 0.035 + mast_h.
ROBOTS = {
    'pebble':   dict(mast_h=0.04, cam_h=0.06, body_rgba='0.9 0.6 0.1 1'),   # short  (~0.30 m lidar)
    'nomad':    dict(mast_h=0.15, cam_h=0.10, body_rgba='0.1 0.3 0.8 1'),   # medium (~0.40 m lidar)
    'sentinel': dict(mast_h=0.65, cam_h=0.55, body_rgba='0.2 0.6 0.3 1'),   # tall   (~0.90 m lidar)
}


def _rsp(context):
    name = LaunchConfiguration('robot').perform(context)
    if name not in ROBOTS:
        raise RuntimeError(f"unknown robot '{name}', choose from {list(ROBOTS)}")
    xacro_file = os.path.join(get_package_share_directory('indoor_nav_description'),
                              'urdf', 'robot.urdf.xacro')
    mappings = {'robot_name': name, **{k: str(v) for k, v in ROBOTS[name].items()}}
    urdf = xacro.process_file(xacro_file, mappings=mappings).toxml()
    return [Node(package='robot_state_publisher', executable='robot_state_publisher',
                 parameters=[{'robot_description': urdf,
                              'use_sim_time': LaunchConfiguration('use_sim_time')}])]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('robot', default_value='nomad', description='pebble | nomad | sentinel'),
        OpaqueFunction(function=_rsp),
    ])
