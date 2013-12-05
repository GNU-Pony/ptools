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

pkgdir  = evald_dirs['destdir']
pkgname = evald_dirs['pkgname']

i_use_info    = get('I_USE_INFO',    'y').lower().startswith('y')
i_use_man     = get('I_USE_MAN',     'y').lower().startswith('y')
i_use_locale  = get('I_USE_LOCALE',  '*')
i_use_license = get('I_USE_LICENSE', 'y').lower().startswith('y')

infodir     = pkgdir + evald_dirs['infodir']
mandir      = pkgdir + evald_dirs['mandir']
localedir   = pkgdir + evald_dirs['localedir']
licensedir  = pkgdir + evald_dirs['licensedir']
datarootdir = pkgdir + evald_dirs['datarootdir']


if not i_use_info:  rm_r(pkgdir + infodir)
if not i_use_man:   rm_r(pkgdir + mandir)
filter_locale(i_use_locale, pkgdir, None, localedir)

if not i_use_license:
    _dir = '%s/%s' % (i_use_license, pkgname)
    if os.path.exists(_dir):
        if os.path.islink(_dir):
            rm(_dir)
        else:
            rm_r(_dir)


if os.path.exists(datarootdir) and os.path.isdir(datarootdir):
    if len(os.listdir(datarootdir)) == 0:
        rmdir(_dir)

