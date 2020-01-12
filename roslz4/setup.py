from setuptools import setup, Extension

include_dirs = [
]

setup(
    name='roslz4',
    packages=['roslz4'],
    version='1.14.3.post0',
    package_dir={'': 'ros_comm/utilities/roslz4/src'},
    install_requires=[],
    ext_package='roslz4',
    ext_modules=[Extension(
        '_roslz4',
        [
            'ros_comm/utilities/roslz4/src/_roslz4module.c',
            'ros_comm/utilities/roslz4/src/lz4s.c',
            'ros_comm/utilities/roslz4/src/xxhash.c',
        ],
        include_dirs=[
            'include',
            'roscpp_core/cpp_common/include',
        ],
        extra_compile_args=[
            '-Wno-strict-prototypes',
            '-Wno-missing-field-initializers',
            '-Wno-unused-variable',
            '-Wno-strict-aliasing',
        ],
        define_macros=[
            ('XXH_NAMESPACE', 'ROSLZ4_'),
        ],
        libraries=['lz4']
    )],
    )
