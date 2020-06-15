#!/bin/bash
# The order matters, so requriments.txt cannot work
pip3 install -U -e "git+https://github.com/ros-infrastructure/catkin_pkg.git#egg=0.4.13"
pip3 install -U -e "git+https://github.com/ros/genmsg.git#egg=0.5.12"
pip3 install -U -e "git+https://github.com/ros/genpy.git#egg=0.6.12"
pip3 install pyyaml setuptools gitpython sip
pip install setuptools
