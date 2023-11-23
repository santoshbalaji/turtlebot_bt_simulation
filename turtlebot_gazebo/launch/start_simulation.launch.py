import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution
 
def generate_launch_description():

  current_pkg_name = 'turtlebot_gazebo'
  gazebo_pkg_name = 'gazebo_ros'

  gazebo_ros_pkg_share = FindPackageShare(package=gazebo_pkg_name).find(gazebo_pkg_name)
  current_pkg_share = FindPackageShare(package=current_pkg_name).find(current_pkg_name)

  # path for turtlebot urdf
  urdf_path = os.path.join(
    get_package_share_directory(current_pkg_name), 'urdf', 'turtlebot3_burger.urdf')
  # path for turtlebot model
  model_path =  os.path.join(
    get_package_share_directory(current_pkg_name), 'model', 'turtlebot3_burger', 'model.sdf')

  with open(urdf_path, 'r') as infp:
    robot_desc = infp.read()

  # path for world file
  world_path = os.path.join(current_pkg_share, 'world', 'small_room.world')

  # path for rviz config file
  rviz_config_path = PathJoinSubstitution([FindPackageShare(current_pkg_name), "rviz", "view_robot.rviz"])

  # adding gazebo model path into the environment for the newly created ones
  gazebo_models_path = os.path.join(current_pkg_share, 'model')
  os.environ["GAZEBO_MODEL_PATH"] = gazebo_models_path

  # launch file to include gazebo launch file to start the gazebo server
  start_gazebo_server_cmd = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(gazebo_ros_pkg_share, 'launch', 'gzserver.launch.py')),
    launch_arguments={'world': world_path}.items())

  # launch file to include gazebo launch file to start the gazebo client
  start_gazebo_client_cmd = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(gazebo_ros_pkg_share, 'launch', 'gzclient.launch.py')))

  # node to publish robot joint states
  robot_state_publisher_cmd =  Node(
    package='robot_state_publisher',
      executable='robot_state_publisher',
      name='robot_state_publisher',
      output='screen',
      parameters=[{
        'use_sim_time': True,
        'robot_description': robot_desc
      }],
  )

  # node to spawn turtlebot model in gazebo
  start_gazebo_ros_spawner_cmd = Node(
    package='gazebo_ros',
    executable='spawn_entity.py',
    arguments=[
        '-entity', 'turtlebot3_burger',
        '-file', model_path,
        '-x', '2.00',
        '-y', '0.00',
        '-z', '0.01'
    ],
    output='screen',
  )

  # node to start rviz
  rviz_node_cmd = Node(
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

  ld.add_action(start_gazebo_server_cmd)
  ld.add_action(start_gazebo_client_cmd)
  ld.add_action(robot_state_publisher_cmd)
  ld.add_action(start_gazebo_ros_spawner_cmd)
  ld.add_action(rviz_node_cmd)

  return ld