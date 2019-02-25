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

# install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub |  apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' |  tee /etc/apt/sources.list.d/google-chrome.list
RUN apt update
RUN apt install -y google-chrome-stable

# install Robotics Language
RUN pip install --upgrade RoboticsLanguage

# install tensor flow
RUN python2 -m pip install --ignore-installed --upgrade tensorflow==1.10.1

# install h5 file reader
RUN pip install h5py

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


RUN echo '"\eOA": history-search-backward\n"\eOB": history-search-forward\n"\e[A": history-search-backward\n"\e[B": history-search-forward\n' > /home/roboticslanguage/.inputrc

# set the development path
RUN mkdir -p /home/roboticslanguage/.rol
RUN echo 'globals:\n  deploy: /home/roboticslanguage/catkin_ws/src/' > /home/roboticslanguage/.rol/parameters.yaml

# copy examples
RUN mkdir -p /home/roboticslanguage/examples
WORKDIR /home/roboticslanguage/examples
RUN rol --copy-examples-here
WORKDIR /home/roboticslanguage
