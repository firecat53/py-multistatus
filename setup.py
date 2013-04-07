"""Copyright 2013 by Scott Hansen <firecat4153 @gmail.com

This file is part of py-multistatus.

Py-multistatus is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

Py-multistatus is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
Py-multistatus.  If not, see <http://www.gnu.org/licenses/>.

"""

from distutils.core import setup

setup(name="py-multistatus",
      version="0.1",
      author="Scott Hansen",
      author_email="firecat4153@gmail.com",
      url="http://firecat53.github.com/py-multistatus",
      description="A multi-interval statusbar information script for use with statusbars like bar and dzen",
      long_description=(open('README.rst').read()),
      packages=['lib', 'plugins'],
      scripts=['bin/multistatus'],
      classifiers=[
          'Programming Language :: Python :: 3',
          'Operating System :: POSIX',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Development Status :: 3 - Alpha',
          'Environment :: System :: Monitoring',
          'Environment :: X11 Applications'],
      data_files=[('share/py-multistatus', ['README.rst',
                                            'COPYING',
                                            'status.cfg',
                                            'monsterstart.py'])]
      )
