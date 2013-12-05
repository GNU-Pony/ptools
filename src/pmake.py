#!/usr/bin/env python3
'''
ptools – software package installation tools

Copyright © 2013  Mattias Andrée (maandree@member.fsf.org)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import sys
import os

try:
    SPIKE_PATH = os.getenv('SPIKE_PATH')
    sys.path.append('%s/src' % SPIKE_PATH)
    from dragonsuite import *
except:
    print('Environment variable SPIKE_PATH has not been set correctly')
    sys.exit(1)


from fh import *

args = []
args.append('DESTDIR='   + evald_dirs['destdir'])
args.append('DIST_ROOT=' + evald_dirs['destdir'])
args.append('PREFIX=' + evald_dirs['exec_prefix'])

make(args + extra_args)

