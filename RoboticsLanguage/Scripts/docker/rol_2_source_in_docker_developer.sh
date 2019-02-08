#!/bin/bash

# setup the environment
source /opt/ros/bouncy/setup.bash

# install pip
curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py
rm get-pip.py

# install the Tools
pip3 install -U colcon-common-extensions

# install the Robotics Language
pip install -e .

# create the catkin workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/

# make sure .bashrc loads ros
echo 'source ~/ros2_ws/install/setup.bash' >> ~/.bashrc

# set the development path
mkdir -p ~/.rol
echo 'globals:
  deploy: /root/ros2_ws/src/deploy
  output: "Ros2Cpp"' > ~/.rol/parameters.yaml

# compile the example
rol /RoL/RoboticsLanguage/Examples/helloworld.rol -c

# source the new code to be able to launch
source ~/ros2_ws/install/setup.bash

cd /RoL
