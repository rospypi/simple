from setuptools import setup
setup(
    name='rospy-builder',
    version='1.0',
    description='rospy package build tool',
    author='Tamamki Nishino',
    author_email='otamachan@gmail.com',
    url='https://otamachan.github.io/rospy-index',
    packages=['rospy_builder'],
    install_requires=[
        'catkin_pkg',
        'genmsg',
        'genpy<2000',
        'pyyaml',
        'setuptools',
        'gitpython',
        ],
    entry_points={
        'console_scripts': [
            'rospy-build = rospy_builder.build:main',
        ],
    },
)
