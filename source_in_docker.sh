#!/bin/bash

# setup the environment
source /opt/ros/kinetic/setup.bash

# compile the example
rol ~/RoboticsLanguage/RoboticsLanguage/Examples/helloworld.rol -c

# source the new code to be able to launch
source ~/catkin_ws/devel/setup.bash

cd ~/RoboticsLanguage/RoboticsLanguage/Examples
