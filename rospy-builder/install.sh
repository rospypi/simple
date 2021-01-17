#!/bin/bash
# The order matters, so requriments.txt cannot work
pip3 install -U -e "git+https://github.com/ros-infrastructure/catkin_pkg.git@0.4.13#egg=catkin_pkg"
pip3 install -U -e "git+https://github.com/ros/genmsg.git@0.5.16#egg=genmsg"
pip3 install -U -e "git+https://github.com/ros/genpy.git@6aad61b699057e85625fb03a93f5abeaf7ec609b#egg=genpy"
pip3 install pyyaml setuptools gitpython sip
pip install setuptools
