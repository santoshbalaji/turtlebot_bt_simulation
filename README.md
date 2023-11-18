# turtlebot_bt_simulation
This repository is for simulation the actions of turtlebot with behavior trees

## Dependencies involved
- [ ] robot_state_publisher

## Install dependencies
```
  rosdep install --from-paths src/turtlebot_bt_simulation -y --ignore-src
```

## Build and Execution
- To build the package

```
  colcon build --packages-select turtlebot_bt_simulation
```

- To visualize the robot in rviz
```
  ros2 launch turtlebot_bt_simulation start_simulation.launch.py
```