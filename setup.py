#!/usr/bin/env python3
#
# Copyright (c) 2015 SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com

from os import path
# Always prefer setuptools over distutils
from setuptools import setup, find_packages


HERE = path.abspath(path.dirname(__file__))

setupdict = dict(
   name='rstxml2db',
   version='0.0.3',
   description='',
   url='https://github.com/tomschr/rstxml2docbook',
   # Author details
   author='Thomas Schraitle',
   author_email='toms (AT) opensuse.org',
   license='GPL-3.0',
   classifiers=[
      'Development Status :: 3 - Alpha',
      'Topic :: Documentation',
      'Topic :: Software Development :: Documentation',
      'Intended Audience :: Developers',
      # Supported Python versions
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
   ],
   keywords='docbook sphinx RST XML',
   include_package_data = True,
   # You can just specify the packages manually here if your project is
   # simple. Or you can use find_packages().
   packages=find_packages('src'),
   package_dir={'': 'src'},
   install_requires=['lxml'],

   # If there are data files included in your packages that need to be
   # installed, specify them here.  If using Python 2.6 or less, then these
   # have to be included in MANIFEST.in as well.
   package_data={
        '': ['src/rstxml2db/*.xsl'],
   },
   entry_points={
        'console_scripts': [
            'rstxml2db=rstxml2db:main',
            'rstxml2docbook=rstxml2db:main',
        ],
    },
)

setup(**setupdict)
