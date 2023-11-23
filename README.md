# turtlebot_bt_simulation
This repository is for simulating actions of turtlebot with behavior trees

## Dependencies involved
- [ ] robot_state_publisher
- [ ] gazebo_ros
- [ ] slam_toolbox

## Install dependencies
- To install dependencies for turtlebot_gazebo package
```
  rosdep install --from-paths src/turtlebot_gazebo -y --ignore-src
```

- To install dependencies for turtlebot_nav2 package
```
  rosdep install --from-paths src/turtlebot_nav2 -y --ignore-src
```

## Build and Execution
- To build the package
```
  colcon build --symlink-install
```

- To start simulation
```
  ros2 launch turtlebot_gazebo start_simulation.launch.py
```

- To start mapping with slam_toolbox
```
  ros2 launch turtlebot_nav2 start_mapping.launch.py
```
