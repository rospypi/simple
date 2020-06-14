import os
import platform
from setuptools import setup, Extension

include_dirs = [
    "geometry2/tf2/include",
    "roscpp_core/cpp_common/include",
    "roscpp_core/rostime/include",
    "stubs/include",
]
library_dirs = []
libraris = []

if "BOOST_ROOT" in os.environ:
    include_dirs += [os.environ["BOOST_ROOT"] + "/include"]
    library_dirs += [os.environ["BOOST_ROOT"] + "/lib"]

if "BOOST_ROOT_1_69_0" in os.environ:
    include_dirs += [os.environ["BOOST_ROOT_1_69_0"] + "/include"]
    library_dirs += [os.environ["BOOST_ROOT_1_69_0"] + "/lib"]

define_macros = [
    ("BOOST_SYSTEM_NO_DEPRECATED", None),
    ("BOOST_ERROR_CODE_HEADER_ONLY", None)]

if platform.system() == "Windows":
    define_macros += [("_WINDOWS", None)]

setup(
    name="tf2_py",
    packages=["tf2_py"],
    version="0.6.5.post0",
    package_dir={"": "geometry2/tf2_py/src"},
    install_requires=["rospy", "geometry_msgs", "tf2_msgs"],
    ext_package="tf2_py",
    ext_modules=[Extension(
        "_tf2",
        [
            "geometry2/tf2_py/src/tf2_py.cpp",
            "geometry2/tf2/src/buffer_core.cpp",
            "geometry2/tf2/src/cache.cpp",
            "geometry2/tf2/src/static_cache.cpp",
            "roscpp_core/rostime/src/time.cpp",
            "roscpp_core/rostime/src/duration.cpp",
        ],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        define_macros=define_macros,
        )],
    )
