import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from launch.event_handlers import OnProcessExit



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='articubot_one' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()

    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    world = LaunchConfiguration('world')
   # world_file_name ='test.world'
   # world_path = os.path.join(get_package_share_directory(package_name),'worlds',world_file_name)
   # declare_world_cmd = DeclareLaunchArgument(
   # name='world',
   # default_value=world_path,
   # description='Full path to the world model file to load')
    
    gazebo_params_file = os.path.join(get_package_share_directory(package_name),'config','gazebo_params.yaml')

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

#    robot_controllers = PathJoinSubstitution(
 #    [
 #           FindPackageShare("package_name"),
  #          "config",
  #          #"diffbot_controllers.yaml",
   #         "my_controllers.yaml"
  #      ]
  #  )
    control_node = Node(
       package="controller_manager",
        executable="ros2_control_node",
  #      parameters=[robot_controllers],
  #      output="both",
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    delay_diff_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
           # target_action=diff_drive_spawner,
            target_action=spawn_entity,
           # on_exit=[control_node],
           on_exit=[diff_drive_spawner],

        )
    )
    delay_joint_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_broad_spawner,
            on_exit=[control_node],
        )
    )

    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        control_node,
        spawn_entity,
        delay_joint_spawner,
        delay_diff_spawner,
        #diff_drive_spawner,
        #joint_broad_spawner
    ])
