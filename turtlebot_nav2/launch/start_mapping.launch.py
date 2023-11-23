import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
  current_pkg_name = 'turtlebot_nav2'

  # path for rviz config file
  rviz_config_path = PathJoinSubstitution([FindPackageShare(current_pkg_name), "rviz", "view_robot.rviz"])
  # path for slam config file
  slam_mapping_config_path = PathJoinSubstitution([FindPackageShare(current_pkg_name), "config", "mapping.yaml"])

  # node for starting slam toolbox
  # it starts in mapping mode if map topic is not giving any map
  start_async_slam_toolbox_node = Node(
      parameters=[
        slam_mapping_config_path,
        {'use_sim_time': True},
      ],
      package='slam_toolbox',
      executable='async_slam_toolbox_node',
      name='slam_toolbox',
      output='screen')
  
  # node for starting rviz
  rviz_node = Node(
    parameters=[
      {'use_sim_time': True},
    ],
    package="rviz2",
    executable="rviz2",
    name="rviz2",
    output="screen",
    arguments=["-d", rviz_config_path],
  )

  ld = LaunchDescription()

  ld.add_action(start_async_slam_toolbox_node)
  ld.add_action(rviz_node)

  return ld
