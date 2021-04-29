import glob
import os
import platform
from setuptools import setup, Extension


orocos_root = "orocos_kinematics_dynamics/"
include_dirs = [
    ".",
    "include",
    "include/kdl",
    orocos_root + "python_orocos_kdl/pybind11/include",
    "/usr/include/eigen3",
]

if "EIGEN_ROOT" in os.environ:
    include_dirs += [os.environ["EIGEN_ROOT"]]

if platform.system() == "Darwin":
    include_dirs += ["/usr/local/include/eigen3"]

extra_compile_args = []
if platform.system() != "Windows":
    extra_compile_args += ["-std=c++11"]

setup(
    name="PyKDL",
    packages=["PyKDL"],
    version="1.5",
    ext_package="PyKDL",
    ext_modules=[Extension(
        "PyKDL",
        glob.glob(orocos_root + "python_orocos_kdl/PyKDL/*.cpp") +
        glob.glob(orocos_root + "orocos_kdl/src/*.cpp") +
        glob.glob(orocos_root + "orocos_kdl/src/utilities/*.cpp") +
        glob.glob(orocos_root + "orocos_kdl/src/utilities/*.cxx"),
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args,
    )],
    zip_safe=False,
)
