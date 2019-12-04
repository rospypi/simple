# This makefile is only for test
all:
	gcc --shared -fPIC -o _roslz4.so \
		-fpermissive \
		-Wno-missing-field-initializers -Wno-unused-variable -Wno-strict-aliasing \
		ros_comm/utilities/roslz4/src/_roslz4module.c \
		ros_comm/utilities/roslz4/src/lz4s.c \
		ros_comm/utilities/roslz4/src/xxhash.c \
		-Iros_comm/utilities/roslz4/include \
		-Iroscpp_core/cpp_common/include \
		`pkg-config --cflags --libs liblz4` \
		`pkg-config --cflags --libs python3`
