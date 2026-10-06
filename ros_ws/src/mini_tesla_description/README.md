# mini_tesla_description

URDF/xacro, meshes and a Gazebo Harmonic simulation of the **Mini Tesla 10C4I** (FINAL rev 2 chassis), for ROS 2 Jazzy.

## Install and build

```bash
sudo apt install ros-jazzy-ros-gz ros-jazzy-xacro ros-jazzy-joint-state-publisher-gui \
                 ros-jazzy-teleop-twist-keyboard
cd ~/ros2_ws/src && unzip mini_tesla_description.zip
cd ~/ros2_ws && colcon build --packages-select mini_tesla_description && source install/setup.bash
```

## Run

```bash
# model only, joint sliders + RViz
ros2 launch mini_tesla_description display.launch.py

# Gazebo Harmonic + bridge + RViz
ros2 launch mini_tesla_description sim.launch.py
# drive it (holonomic: hold Shift for strafing keys)
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Launch arguments (`sim.launch.py`):

| Argument | Default | Meaning |
| --- | --- | --- |
| `drive` | `mecanum` | `mecanum`: real wheel contact + gz MecanumDrive. `planar`: ideal holonomic base (VelocityControl), use if contact tuning gives you trouble |
| `side_radars` | `false` | radars on both side extensions |
| `rear_radar` | `false` | radar on the rear bumper |
| `laptop` | `true` | G14 on the deck (1.5 kg, changes the CoG a lot) |
| `world` | `worlds/test_arena.sdf` | 6 x 6 m arena with obstacles |
| `rviz` | `true` | open RViz |
| `x`, `y`, `yaw` | `0` | spawn pose |

## Frames

`odom -> base_footprint` (floor, robot centre) `-> base_link` (chassis underside centre, +21 mm; same origin as the CAD)
-> `*_wheel_link`, `tof_<name>_link`, `radar_<name>_link`, `oak_link` -> `oak_optical_frame`, `oak_imu_link`,
`deck_link`, `battery_link`, `laptop_link`. Sensor frames look along +X; the optical frame along +Z.

## Topics (ROS side)

| Topic | Type | Notes |
| --- | --- | --- |
| `/cmd_vel` | `geometry_msgs/Twist` | in: vx, vy, wz |
| `/odom`, `/tf` | `nav_msgs/Odometry`, `tf2_msgs/TFMessage` | odom -> base_footprint, 50 Hz |
| `/joint_states` | `sensor_msgs/JointState` | 4 wheel joints |
| `/tof/<name>/scan` | `sensor_msgs/LaserScan` | 8 ToFs: `front_left/right`, `rear_left/right`, `left_front/rear`, `right_front/rear` |
| `/tof/<name>/range` | `sensor_msgs/Range` | nearest beam, like the real VL53L1X (from `tof_to_range.py`) |
| `/radar/front/points` | `sensor_msgs/PointCloud2` | also `left`, `right`, `rear` when enabled |
| `/oak/rgb/image_raw`, `/oak/rgb/camera_info` | `Image`, `CameraInfo` | 640x480 @ 30 Hz |
| `/oak/depth/image_raw`, `/oak/points` | `Image` (32FC1), `PointCloud2` | depth 0.2-10 m |
| `/oak/imu` | `sensor_msgs/Imu` | 200 Hz |
| `/clock` | `rosgraph_msgs/Clock` | everything runs with `use_sim_time` |

## What is real and what is approximated

- **Geometry is from the CAD**: wheel positions (x +-133.05, y +-134.4 mm, 75 mm wheels), every sensor position
  and direction, the camera, deck and laptop. Visual meshes are exported from the CAD and simplified.
- **Collisions are simple boxes**, and wheels are spheres, so contact stays fast and stable.
- **Masses are estimates** (printed volume x 1.25 g/cc x ~60 % fill, plus the bought parts): about 5.5 kg total
  with the laptop. Weigh the real robot and update the `m_*` properties in `urdf/mini_tesla.urdf.xacro`.
- **Mecanum wheels** are modelled the way gz-sim's own mecanum demo does it: each wheel grips only along a
  45 deg direction fixed in the chassis frame (`fdir1 gz:expressed_in="base_footprint"`, `mu = 1`, `mu2 = 0`).
- **Gazebo has no ToF or mmWave radar sensor.** The ToFs are 5-beam gpu_lidars over the real 27 deg FoV (0.04-4 m),
  and the radar is a 64 x 8 gpu_lidar over 120 x 40 deg (0.1-10 m). That gives correct geometry and range but
  no Doppler, multipath or material effects.
- Motor limits: 55 rad/s (530 rpm no-load) and 0.6 N m per wheel; the drive is capped at 1.5 m/s.

## Troubleshooting

- **Robot spins or drifts in mecanum mode:** try `drive:=planar` to separate contact problems from your stack.
- **No sensor data:** the world must load the `Sensors` (ogre2) and `Imu` systems. `test_arena.sdf` does; copy
  those plugin lines into your own worlds.
- **Meshes missing in Gazebo:** the URDF uses absolute `file://` paths from `$(find mini_tesla_description)`,
  so rebuild after moving the workspace.
