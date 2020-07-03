# This makefile is only for test
all:
	g++ --shared -fPIC -o PyKDL.so \
		-std=c++14 \
		-I. \
		-Iinclude \
		-Iinclude/kdl \
		-Iorocos_kinematics_dynamics/python_orocos_kdl/pybind11/include \
		orocos_kinematics_dynamics/python_orocos_kdl/PyKDL/pybind11/*.cpp \
		orocos_kinematics_dynamics/orocos_kdl/src/*.cpp \
		orocos_kinematics_dynamics/orocos_kdl/src/utilities/*.cpp \
		orocos_kinematics_dynamics/orocos_kdl/src/utilities/*.cxx \
		`pkg-config --cflags --libs eigen3` \
		`pkg-config --cflags --libs python3`
