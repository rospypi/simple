# **THIS IS NOT THE OFFICIAL ROSPY INDEX SERVER**

# rospy for pure Python

## What is this for?

``rospy`` [packages](https://rospypi.github.io/simple/) without ROS installation.
It can be run in a pure python virtualenv.
It also supports ``tf2`` and other binary packages.

Supported Python versions: 3.6, 3.7, 3.8

Support platforms: Linux, Windows, MacOSX

(Not all packages are tested.)

## Install

```bash
virtualenv -p python3 venv
. ./venv/bin/activate
pip install --extra-index-url https://rospypi.github.io/simple/ rospy
pip install --extra-index-url https://rospypi.github.io/simple/ tf2_ros
```

## Sample

```python
import rospy
import std_msgs.msg


def callback(msg):
    print(msg)


rospy.init_node("hoge")
rospy.loginfo('start')
sub = rospy.Subscriber("sub", std_msgs.msg.String, callback)
pub = rospy.Publisher('pub', std_msgs.msg.Int16, queue_size=10)
rate = rospy.Rate(1)
while not rospy.is_shutdown():
    pub.publish(3)
    rate.sleep()
```

Enjoy!

## Start a local pypi server

```bash
docker build -t localpypi .
docker run --rm -p 8000:8000 localpypi
```

```bash
virtualenv -p python3 venv
. ./venv/bin/activate
pip install --extra-index-url http://localhost:8000/index/ rospy
```


## Development

``build.py`` downloads packages from github.com, builds wheel files and generates a Python package server directory.

```bash
git submodule update --init --recursive
# create virtualenv for build packages
virtualenv -p python3 dev
. ./dev/bin/activate
pip install --extra-index-url https://rospypi.github.io/simple/ -e rospy-builder/
# build pure python packages
rospy-build build -d any
# build platform depended packages if you need
rospy-build build -d linux --native
```

To build index html files, use [rospypi/index\_builder](https://github.com/rospypi/index_builder).
```
pip3 install git+git://github.com/rospypi/index_builder.git
python3 -m index_builder local index/ any/ linux/
python -m http.server
```

```bash
virtualenv -p python3 venv
. ./venv/bin/activate
pip install --extra-index-url http://localhost:8000/index/ rospy
```

## Generate Message Python Package

```bash
git clone https://github.com/rospypi/simple.git
cd simple
virtualenv -p python3 venv
. ./venv/bin/activate
pip install --extra-index-url https://rospypi.github.io/simple/ -e rospy-builder/
mkdir msgs
(cd msgs; git clone https://github.com/ros/std_msgs.git)
(cd msgs; git clone https://github.com/ros/common_msgs.git)
# (cd msgs; any repository that is depended on your message)
rospy-build genmsg your_package_path -s msgs/
# ex.rospy-build genmsg ros_tutorials/rospy_tutorials/ -s msgs/
```
