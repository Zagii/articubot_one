import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription

from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

import xacro


def generate_launch_description():
    

    # this name has to match the robot name in the Xacro file
    robotXacroName='robot'

    # this is the name of our package, at the same time this is the name of the 
    # folder that will be used to define the paths
    namePackage = 'articubot_one'
    # this is a relative path to the xacro file defining the model
    modelFileRelativePath = 'description/robot.urdf.xacro'

    # this is the absolute path to the model
    pathModelFile = os.path.join(get_package_share_directory(namePackage),modelFileRelativePath)

    # get the robot description from the xacro model file
    robotDescription = xacro.process_file(pathModelFile).toxml()

    # Check if we're told to use sim time
    use_sim_time = True # LaunchConfiguration('use_sim_time')

    
    
    # Create a robot_state_publisher node
    params = {'robot_description': robotDescription, 'use_sim_time': use_sim_time}
    nodeRobotStatePublisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    ld = LaunchDescription()
    ld.add_action(nodeRobotStatePublisher)

    # Launch!
    return ld
