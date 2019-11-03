FROM osrf/ros:melodic-desktop

# install pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN rm get-pip.py
RUN pip install --upgrade pip

# Update package list
RUN apt update

# Install several useful packages
RUN apt install -y python-catkin-tools python-catkin-lint
RUN apt install -y xterm git sudo build-essential
RUN apt install -y apt-utils curl nano cmake python ssh bash-completion iputils-ping
RUN apt install -y python-argcomplete
RUN activate-global-python-argcomplete

# install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub |  apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' |  tee /etc/apt/sources.list.d/google-chrome.list
RUN apt update
RUN apt install -y google-chrome-stable

# install tensor flow
RUN python2 -m pip install --ignore-installed --upgrade tensorflow==1.10.1

# install h5 file reader
RUN pip install h5py

# install ros bridge server
RUN apt install -y ros-melodic-rosbridge-server


# Create roboticslanguage user and add it to sudoers
RUN adduser --disabled-password --gecos "" ubuntu
RUN echo 'ubuntu:me' | chpasswd
RUN usermod -a -G sudo,dialout ubuntu
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers #ubuntu can always sudo without password


# install colcon
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
RUN apt update
RUN apt install -y python3-colcon-common-extensions
RUN apt install -y python3-pip
RUN pip3 install setuptools

# set default user when running the container
USER ubuntu

# get aws examples
RUN mkdir -p /home/ubuntu/environment/aws

WORKDIR /home/ubuntu/environment/aws

RUN git clone https://github.com/aws-robotics/aws-robomaker-small-house-world.git
RUN git clone https://github.com/aws-robotics/aws-robomaker-bookstore-world.git
RUN git clone https://github.com/aws-robotics/aws-robomaker-sample-application-helloworld.git
RUN git clone https://github.com/aws-robotics/aws-robomaker-sample-application-open-source-rover.git
RUN git clone https://github.com/aws-robotics/aws-robomaker-sample-application-objecttracker.git
RUN git clone https://github.com/aws-robotics/aws-robomaker-sample-application-persondetection.git
RUN git clone https://github.com/aws-robotics/utils-common.git
RUN git clone https://github.com/aws-robotics/aws-robomaker-racetrack-world.git
RUN git clone https://github.com/aws-robotics/aws-iot-bridge-example.git
RUN git clone https://github.com/aws-robotics/utils-ros1.git
RUN git clone https://github.com/aws-robotics/monitoringmessages-ros1.git
RUN git clone https://github.com/aws-robotics/aws-robomaker-sample-application-deepracer.git
RUN git clone https://github.com/aws-robotics/aws-robomaker-simulation-ros-pkgs.git
RUN git clone https://github.com/aws-robotics/aws-robomaker-sample-application-cloudwatch.git
RUN git clone https://github.com/aws-robotics/aws-robomaker-sample-application-voiceinteraction.git

WORKDIR /home/ubuntu


# make sure .bashrc loads ros
RUN echo 'source /opt/ros/melodic/setup.bash' >> /home/ubuntu/.bashrc


RUN echo '"\eOA": history-search-backward\n"\eOB": history-search-forward\n"\e[A": history-search-backward\n"\e[B": history-search-forward\n' > /home/ubuntu/.inputrc

USER root

# install Robotics Language
RUN echo "Installing rol...."
RUN pip install --upgrade RoboticsLanguage

USER ubuntu
WORKDIR /home/ubuntu

# set the environment
RUN rol --set-environment AWSRobomakerHelloWorld

WORKDIR /home/ubuntu/environment
RUN ln -s aws/aws-robomaker-sample-application-helloworld HelloWorld

RUN echo 'ok'
USER root
#


RUN curl -sSL http://get.gazebosim.org | sh

# RUN sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" /etc/apt/sources.list.d/gazebo-stable.list'
# RUN wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
#
#
# RUN sudo apt-get update
#
# RUN sudo apt-get install ros-melodic-gazebo9-*
#
USER ubuntu
