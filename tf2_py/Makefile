# This makefile is only for test
all:
	g++ --shared -fPIC -o _tf2.so \
		-std=c++14 \
		-DBOOST_SYSTEM_NO_DEPRECATED \
		-DBOOST_ERROR_CODE_HEADER_ONLY \
		geometry2/tf2_py/src/tf2_py.cpp \
		geometry2/tf2/src/buffer_core.cpp \
		geometry2/tf2/src/cache.cpp \
		geometry2/tf2/src/static_cache.cpp \
		roscpp_core/rostime/src/time.cpp \
		roscpp_core/rostime/src/duration.cpp \
		-Igeometry2/tf2/include \
		-Iroscpp_core/cpp_common/include \
		-Iroscpp_core/rostime/include \
		-Istubs/include \
		`pkg-config --cflags --libs python3`
