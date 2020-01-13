from setuptools import setup

setup(
    name="rospy-builder",
    version="0.2.0",
    description="rospy package build tool",
    author="Tamamki Nishino",
    author_email="otamachan@gmail.com",
    url="https://rospypi.github.io/simple",
    packages=["rospy_builder"],
    install_requires=[
        "catkin_pkg",
        "click",
        "genmsg",
        "genpy<2000",
        "pyyaml",
        "setuptools",
        "gitpython",
    ],
    entry_points={
        "console_scripts": ["rospy-build = rospy_builder.build:cli",],
    },
)
