#!/usr/bin/env python
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup()

d['packages'] = ['cv_bridge', 'cv_bridge.boost']
d['package_dir'] = {'' : 'python'}
d['version'] += ".post1"

setup(**d)
