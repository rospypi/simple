from setuptools import setup
import sys

install_requires = [
    "catkin_pkg",
    "click",
    "genmsg",
    "genpy<2000",
    "pyyaml",
    "setuptools",
    "gitpython",
]

if sys.version_info < (3, 7):
    install_requires.append("dataclasses>=0.7,<1")

setup(
    name="rospy-builder",
    version="0.3.0",
    description="rospy package build tool",
    author="Tamamki Nishino",
    author_email="otamachan@gmail.com",
    url="https://rospypi.github.io/simple",
    packages=["rospy_builder"],
    install_requires=install_requires,
    entry_points={
        "console_scripts": ["rospy-build = rospy_builder.build:cli",],
    },
)
