FROM osrf/ros:kinetic-desktop

# Install required wget for adding other repos
RUN curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py
