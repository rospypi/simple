# This makefile is only for test
all:
	g++ --shared -fPIC -o PyKDL.so \
		-std=c++14 \
		-I. \
		*.cpp \
		orocos_kinematics_dynamics/orocos_kdl/src/*.cpp \
		orocos_kinematics_dynamics/orocos_kdl/src/utilities/*.cpp \
		orocos_kinematics_dynamics/orocos_kdl/src/utilities/*.cxx \
		`pkg-config --cflags --libs eigen3` \
		`pkg-config --cflags --libs python3`
