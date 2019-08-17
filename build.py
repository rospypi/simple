#!/usr/bin/env python
import argparse
import os
import pathlib
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
from urllib.request import urlopen
import zipfile

from typing import Optional


def download_from_github(
        dest: pathlib.Path,
        repo: str,
        ver: str) -> pathlib.Path:
    url = 'https://github.com/{0}/archive/{1}.zip'.format(repo, ver)
    zip_file = dest / '{0}_{1}.zip'.format(repo.split('/')[1], ver)
    if not zip_file.exists():
        u = urlopen(url)
        with open(zip_file, 'wb') as outs:
            block_sz = 8192
            while True:
                buf = u.read(block_sz)
                if not buf:
                    break
                outs.write(buf)
    return zip_file


def unzip(
        zip_file: pathlib.Path,
        dest: pathlib.Path,
        subdir: Optional[pathlib.Path]=None) -> None:
    with open(zip_file, 'rb') as f:
        zipfp = zipfile.ZipFile(f)
        for zip_file_name in zipfp.namelist():
            original = pathlib.Path(zip_file_name)
            name = pathlib.Path(*original.parts[1:])
            if subdir:
                try:
                    name.relative_to(subdir)
                except ValueError:
                    continue
                fname = dest / pathlib.Path(*name.parts[len(subdir.parts):])
            else:
                fname = dest / name
            data = zipfp.read(zip_file_name)
            if zip_file_name.endswith('/'):
                if not fname.exists():
                    fname.mkdir(parents=True)
            else:
                fname.write_bytes(data)


def build_wheel(path: pathlib.Path, build_py2: bool=False) -> None:
    cwd = os.getcwd()
    try:
        os.chdir(path)
        sys.argv = ['', 'sdist', 'bdist_wheel', '--universal']
        runpy.run_path(path / 'setup.py')
        if build_py2:
            # TODO: find a better way
            subprocess.call(['python2', 'setup.py', 'bdist_wheel'])
    finally:
        os.chdir(cwd)


def generate_rosmsg_from_action(
        dest: pathlib.Path,
        package: str):
    dest_dir = dest / package
    msg_dir = dest_dir / 'msg'
    files = dest_dir.glob('action/*.action')
    for action in files:
        name = action.name[:-7]
        # parse
        parts = [[]]
        for l in action.read_text().split('\n'):
            if l.startswith(u'---'):
                parts.append([])
                continue
            parts[-1].append(l)
        parts = ['\n'.join(p) for p in parts]
        assert len(parts) == 3
        (msg_dir / (name + 'Goal.msg')).write_text(parts[0])
        (msg_dir / (name + 'Result.msg')).write_text(parts[1])
        (msg_dir / (name + 'Feedback.msg')).write_text(parts[2])
        (msg_dir / (name + 'Action.msg')).write_text(u'''
{0}ActionGoal action_goal
{0}ActionResult action_result
{0}ActionFeedback action_feedback
'''.format(name))
        (msg_dir / (name + 'ActionGoal.msg')).write_text(u'''
Header header
actionlib_msgs/GoalID goal_id
{0}Goal goal
'''.format(name))
        (msg_dir / (name + 'ActionResult.msg')).write_text(u'''
Header header
actionlib_msgs/GoalStatus status
{0}Result result
'''.format(name))
        (msg_dir / (name + 'ActionFeedback.msg')).write_text(u'''
Header header
actionlib_msgs/GoalStatus status
{0}Feedback result
'''.format(name))


def generate_rosmsg(
        dest: pathlib.Path,
        package: str,
        version: str,
        search_root_path: Optional[pathlib.Path]=None) -> None:
    import genpy.generator
    import genpy.genpy_main
    search_path = {
        package: [dest / package / 'msg']}
    if search_root_path is not None:
        for msg_path in search_root_path.glob('*/*/msg'):
            search_path[msg_path.parent.name] = [msg_path]
    for gentype in ('msg', 'srv'):
        files = (dest / package / gentype).glob('*.{0}'.format(gentype))
        if files:
            if gentype == 'msg':
                generator = genpy.generator.MsgGenerator()
            elif gentype == 'srv':
                generator = genpy.generator.SrvGenerator()
            ret = generator.generate_messages(
                package,
                files,
                dest / package / gentype,
                search_path)
            if ret:
                raise RuntimeError(
                    'Failed to generate python files from msg files.')
            genpy.generate_initpy.write_modules(
                dest / package / gentype)
        genpy.generate_initpy.write_modules(
            dest / package)
    (dest / 'setup.py').write_text(
        u'from setuptools import find_packages, setup\n'
        'setup(name=\'{0}\', version=\'{1}\', '
        'packages=find_packages(), '
        'install_requires=[\'genpy\'])\n'.
        format(package, version))


def build_wheel_from_github_package(
        dest: pathlib.Path,
        repo: str,
        version: str,
        subdir: Optional[pathlib.Path]=None) -> None:
    if subdir:
        package = subdir.name
    else:
        package = repo.split('/')[1]
    dest_dir = dest / package
    zipfile = download_from_github(dest, repo, version)
    unzip(zipfile, dest_dir, subdir)
    build_wheel(dest_dir)


def build_wheel_from_github_msg(
        dest: pathlib.Path,
        repo: str,
        version: str,
        subdir: Optional[pathlib.Path]=None) -> None:
    if subdir:
        package = subdir.name
    else:
        package = repo.split('/')[1]
    dest_dir = dest / package
    zipfile = download_from_github(dest, repo, version)
    if subdir is None:
        subdir = pathlib.Path()
    unzip(zipfile, dest_dir / package / 'msg', subdir / 'msg')
    unzip(zipfile, dest_dir / package / 'srv', subdir / 'srv')
    unzip(zipfile, dest_dir / package / 'action', subdir / 'action')
    generate_rosmsg_from_action(dest_dir, package)
    generate_rosmsg(dest_dir, package, version, search_root_path=dest)
    build_wheel(dest_dir)


def build_wheel_from_local_package(
        dest: pathlib.Path,
        local_path: pathlib.Path,
        build_py2: bool=False) -> None:
    package = local_path.name
    dest_dir = dest / package
    shutil.rmtree(dest_dir, ignore_errors=True)
    shutil.copytree(local_path, dest_dir)
    build_wheel(dest_dir, build_py2)


def generate_package_index(
        dest: pathlib.Path,
        package_dir: pathlib.Path,
        generate_html: bool) -> bool:
    # https://www.python.org/dev/peps/pep-0503/
    package_dest = dest / re.sub(r"[-_.]+", "-", package_dir.name).lower()
    package_dest.mkdir(parents=True, exist_ok=True)
    files = []
    for f in (package_dir / 'dist').glob('*'):
        print(f.name)
        files.append(f.name)
        shutil.copy(f, package_dest)
    if generate_html:
        files_list = ''.join([
            u'<a href="{0}">{0}</a>'.format(f)
            for f in files])
        (package_dest / 'index.html').write_text(
            u'<!DOCTYPE html><html><body>{0}</body></html>'.format(
                files_list))
    return len(files) != 0


def generate_index(
        dest: pathlib.Path,
        source: pathlib.Path,
        generate_html: bool) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    packages = []
    for package_dir in source.glob('*'):
        if package_dir.is_dir():
            found = generate_package_index(dest, package_dir, generate_html)
            if found:
                packages.append(package_dir.name)
    if generate_html:
        package_list = ''.join([
            u'<a href="/{0}/">{0}</a>'.format(p)
            for p in packages])
        (dest / 'index.html').write_text(
            u'<!DOCTYPE html><html><body>{0}</body></html>'.format(
                package_list))


def build(dest: pathlib.Path, tmp: pathlib.Path) -> None:
    tmp.mkdir(parents=True, exist_ok=True)
    # core rospy packages
    build_wheel_from_local_package(tmp, pathlib.Path('rospy3'))
    build_wheel_from_github_package(
        tmp, 'ros-infrastructure/catkin_pkg', '0.4.13')
    build_wheel_from_github_package(
        tmp, 'ros-infrastructure/rospkg', '1.1.10')
    build_wheel_from_github_package(
        tmp, 'ros/ros', '1.14.6', pathlib.Path('core/roslib'))
    build_wheel_from_github_package(
        tmp, 'ros/genpy', '0.6.8')
    build_wheel_from_github_package(
        tmp, 'ros/genmsg', '0.5.12')
    build_wheel_from_github_package(
            tmp, 'ros/catkin', '0.7.18')
    build_wheel_from_github_package(
        tmp, 'ros/ros_comm', '1.14.3', pathlib.Path('clients/rospy'))
    build_wheel_from_github_package(
        tmp, 'ros/ros_comm', '1.14.3', pathlib.Path('tools/rosgraph'))
    # core ros message packages
    build_wheel_from_github_msg(
        tmp, 'ros/std_msgs', '0.5.12')
    build_wheel_from_github_msg(
        tmp, 'ros/ros_comm', '1.14.3', pathlib.Path('clients/roscpp'))
    build_wheel_from_github_msg(
        tmp, 'ros/ros_comm_msgs', '1.11.2', pathlib.Path('rosgraph_msgs'))
    # extra ros packages
    build_wheel_from_github_package(
        tmp, 'ros/actionlib', '1.12.0')
    # build_wheel_from_github_package(
    #     tmp, 'ros/geometry2', '0.6.5', pathlib.Path('tf2_ros'))
    build_wheel_from_local_package(tmp, pathlib.Path('tf2_py'), True)
    build_wheel_from_local_package(
        tmp, pathlib.Path('tf2_py/geometry2/tf2_ros'))
    # extra ros messages
    common_msgs = [
        'geometry_msgs',
        'sensor_msgs',
        'actionlib_msgs',
        'shape_msgs',
        'diagnostic_msgs',
        'nav_msgs',
        'stereo_msgs',
        'trajectory_msgs',
        'visualization_msgs',
    ]
    for msg in common_msgs:
        build_wheel_from_github_msg(
            tmp, 'ros/common_msgs', '1.12.7', pathlib.Path(msg))
    build_wheel_from_github_msg(
        tmp, 'ros/geometry2', '0.6.5', pathlib.Path('tf2_msgs'))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dest', default='index',
        help='destination directory of artifacts')
    parser.add_argument(
        '-n', '--no-index', action='store_true',
        help='do not generate index files')
    parser.add_argument(
        '-k', '--keep', action='store_true',
        help='keep build files to /tmp/build')
    args = parser.parse_args()
    if args.keep:
        tmp = pathlib.Path(tempfile.gettempdir()) / 'build'
    else:
        tmp = pathlib.Path(tempfile.mkdtemp())
    dest = pathlib.Path(args.dest)
    try:
        build(dest, tmp)
        generate_index(dest, tmp, not args.no_index)
    finally:
        if not args.keep:
            shutil.rmtree(tmp)


if __name__ == '__main__':
    main()
