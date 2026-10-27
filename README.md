# indoor_auto_nav — Stage 1: simulation

ROS 2 Humble + Gazebo Classic 11.

| Package | Contents |
|---|---|
| `indoor_nav_description` | Xacro: diff-drive base, 16-ch 3D lidar (`/points`), RGB-D camera (`/camera/rgbd/*`), RViz config |
| `indoor_nav_gazebo` | 12x8 m house (bedroom, living room, kitchen, office, doorways + furniture/objects), sim launch |

## Run
    cd ~/Pictures/indoor_auto_nav
    colcon build --symlink-install && source install/setup.bash
    ros2 launch indoor_nav_gazebo sim.launch.py            # gui:=false rviz:=false for headless
    ros2 run teleop_twist_keyboard teleop_twist_keyboard   # drive

Regenerate the world: `python3 src/indoor_nav_gazebo/scripts/generate_world.py > src/indoor_nav_gazebo/worlds/indoor_house.world`

## Topics
`/cmd_vel` `/odom` `/tf` `/joint_states` `/points` (PointCloud2, frame `lidar_link`),
`/camera/rgbd/{image_raw,depth/image_raw,points,camera_info}` (frame `camera_optical_link`)
