import glob
import os
import platform
import subprocess
from distutils.cmd import Command
from setuptools import setup, Extension
from setuptools.command.sdist import sdist
from setuptools.command.build_ext import build_ext


orocos_root = "orocos_kinematics_dynamics/"
include_dirs = [
    ".",
    "kdl",
    "kdl/utilities",
    orocos_root + "orocos_kdl/src",
    "/usr/include/eigen3",
]

if "EIGEN_ROOT" in os.environ:
    include_dirs += [os.environ["EIGEN_ROOT"]]

if platform.system() == "Darwin":
    include_dirs += ["/usr/local/include/eigen3"]


class _Extension(Extension):
    def __init__(self, name, sources, sip_file=None, **kwargs):
        Extension.__init__(self, name, sources, **kwargs)
        self.sip_file = sip_file


class gensip(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for ext in self.distribution.ext_modules:
            if isinstance(ext, _Extension):
                if ext.sip_file:
                    sip_dir = "sip_" + ext.name
                    if not os.path.exists(sip_dir):
                        os.makedirs(sip_dir)
                        if platform.system() == "Linux":
                            subprocess.check_output([
                                "sip", "-c", sip_dir, "-o", "-j", "1",
                                ext.sip_file
                            ])
                    ext.sources.extend(glob.glob(sip_dir + "/*.cpp"))
                    ext.include_dirs.append(sip_dir)


class _sdist(sdist):
    def run(self):
        self.run_command("gensip")
        sdist.run(self)


class _build_ext(build_ext):
    def run(self):
        self.run_command("gensip")
        build_ext.run(self)


setup(
    name="PyKDL",
    packages=["PyKDL"],
    version="1.4.post1",
    ext_package="PyKDL",
    ext_modules=[_Extension(
        "PyKDL",
        glob.glob(orocos_root + "orocos_kdl/src/*.cpp") +
        glob.glob(orocos_root + "orocos_kdl/src/utilities/*.cpp") +
        glob.glob(orocos_root + "orocos_kdl/src/utilities/*.cxx"),
        include_dirs=include_dirs,
        sip_file=orocos_root + "python_orocos_kdl/PyKDL/PyKDL.sip",
    )],
    cmdclass={
        "gensip": gensip,
        "sdist": _sdist,
        "build_ext": _build_ext,
    },
    install_requires=["sip<5.0.0"],
    zip_safe=False,
)
