#!/usr/bin/python
# Copyright (C) 2011  Lars Wirzenius
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from distutils.core import setup
import glob
import sys

import cliapp


# Only install manpages in the 3.x version so that the Debian
# packaging doesn't end up having it in two packages.
if sys.version_info > (3,):
    manpages = [('share/man/man5', glob.glob('*.5'))]
else:
    manpages = None


setup(
    name='cliapp',
    version=cliapp.__version__,
    author='Lars Wirzenius',
    author_email='liw@liw.fi',
    url='http://liw.fi/cliapp/',
    description='framework for Unix command line programs',
    long_description='''\
    cliapp makes it easier to write typical Unix command line programs,
    by taking care of the common tasks they need to do, such as
    parsing the command line, reading configuration files, setting
    up logging, iterating over lines of input files, and so on.
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Text Processing :: Filters',
        'Topic :: Utilities',
    ],
    packages=['cliapp'],
    data_files=manpages,
)
