#!/bin/env python
# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
Setup script for pycsync
'''

import os
from setuptools import Command, setup

# Ensure we are in pycsync source dir
setup_dirname = os.path.dirname(__file__)
if setup_dirname != '':
    os.chdir(setup_dirname)

pycsync_version = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                               'pycsync',
                                               'version.py')
pycsync_reqs = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                            'requirements.txt')

exec(compile(open(pycsync_version).read(), pycsync_version, 'exec'))

with open(pycsync_reqs) as f:
    lines = f.read().split('\n')
    requirements = [line for line in lines if line]


class CleanSDist(Command):
    description = "Remove traces of setup.py sdist"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import glob
        import os
        import shutil
        shutil.rmtree('dist', True)
        for EIDIR in glob.glob(os.path.join('pycsync', '*egg*info*')):
            shutil.rmtree(EIDIR, True)


setup_kwargs = {'name': 'pycsync',
                'version': __version__,
                'url': '',
                'license': '',
                'description': 'Open Source BSP Level Creator',
                'author': 'Timothy F Messier',
                'author_email': 'tim.messier@gmail.com',
                'classifiers': ['Programming Language :: Python',
                                'Programming Language :: Python :: 2.7',
                                'Development Status :: 1 - Planning',
                                'Environment :: X11 Applications :: GTK',
                                'Intended Audience :: Developers',
                                'Intended Audience :: End Users/Desktop',
                                ('License :: OSI Approved ::'
                                 ' ISC License (ISCL)'),
                                'Operating System :: POSIX :: Linux',
                                ],
                'packages': ['pycsync'],
                'package_data': {},
                'data_files': [],
                'scripts': ['scripts/pycsync'],
                'install_requires': requirements,
                'zip_safe': False,
                'cmdclass': {'clean_sdist': CleanSDist},
                }

if __name__ == '__main__':
    setup(**setup_kwargs)
