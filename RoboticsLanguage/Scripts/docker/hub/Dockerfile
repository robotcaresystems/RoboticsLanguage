FROM osrf/ros:kinetic-desktop

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

# install Robotics Language
RUN pip install --upgrade RoboticsLanguage

# Create roboticslanguage user and add it to sudoers
RUN adduser --disabled-password --gecos "" roboticslanguage
RUN echo 'roboticslanguage:me' | chpasswd
RUN usermod -a -G sudo,dialout roboticslanguage
RUN echo "roboticslanguage ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers #roboticslanguage can always sudo without password

# set default user when running the container
USER roboticslanguage
WORKDIR /home/roboticslanguage

# create the catkin workspace
RUN mkdir -p /home/roboticslanguage/catkin_ws/src

# make sure .bashrc loads ros
RUN echo 'source /opt/ros/kinetic/setup.bash' >> /home/roboticslanguage/.bashrc
RUN echo 'source /home/roboticslanguage/catkin_ws/devel/setup.bash &> /dev/null' >> /home/roboticslanguage/.bashrc

# set the development path
RUN mkdir -p /home/roboticslanguage/.rol
RUN echo 'globals:\n  deploy: /root/catkin_ws/src/deploy' > /home/roboticslanguage/.rol/parameters.yaml
