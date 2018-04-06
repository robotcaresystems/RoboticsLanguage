FROM osrf/ros:kinetic-desktop

# Install pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py

# install the catkin tools
RUN pip install catkin_tools

# create the catkin workspace
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/ && catkin init

# install the Robotics language
RUN cd ~ && git clone https://github.com/robotcaresystems/RoboticsLanguage.git && cd RoboticsLanguage && pip install -e .

# add the deploy path
RUN mkdir -p ~/.rol && echo "globals:\n  deploy: /root/catkin_ws/src/deploy" > ~/.rol/parameters.yaml
