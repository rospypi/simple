import platform
from setuptools import setup, Extension

extra_compile_args = []
include_dirs = [
    "include",
    "roscpp_core/cpp_common/include",
]
libraries = ["lz4"]
library_dirs = []
define_macros = [
    ("XXH_NAMESPACE", "ROSLZ4_"),
]

if platform.system() == "Windows":
    # these are special value for Github Action build
    include_dirs += ["lz4-1.9.2/lib"]
    libraries = ["lz4-1.9.2/visual/VS2017/liblz4/bin/x64_Release/liblz4_static"]
else:
    extra_compile_args += [
        "-Wno-strict-prototypes",
        "-Wno-missing-field-initializers",
        "-Wno-unused-variable",
        "-Wno-strict-aliasing",
    ]
    if platform.system() == "Darwin":
        extra_compile_args += [""]


setup(
    name="roslz4",
    packages=["roslz4"],
    version="1.14.3.post2",
    package_dir={"": "ros_comm/utilities/roslz4/src"},
    install_requires=[],
    ext_package="roslz4",
    ext_modules=[Extension(
        "_roslz4",
        [
            "ros_comm/utilities/roslz4/src/_roslz4module.c",
            "ros_comm/utilities/roslz4/src/lz4s.c",
            "ros_comm/utilities/roslz4/src/xxhash.c",
        ],
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args,
        define_macros=define_macros,
        libraries=libraries,
        library_dirs=library_dirs,
    )],
    )
