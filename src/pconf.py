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

param_dirs = ['prefix', 'exec-prefix', 'bindir', 'sbindir', 'libexecdir', 'sysconfdir', 
              'sharedstatedir', 'localstatedir', 'libdir', 'includedir', 'oldincludedir', 
              'datarootdir', 'datadir', 'infodir', 'localedir', 'mandir', 'docdir',
              'htmldir', 'dvidir', 'pdfdir', 'psdir']

configure_script = './configure' if (os.path.exists('./configure')) else './Configure'
if 'configure-script' in dirs:
    configure_script = dirs[configure-script]

_bool = lambda opt, dft : '--%sable-%s' % ('en' if get('I_USE_' + opt.upper(), dft).lower().startswith('y') else 'dis', opt)
_with = lambda opt, dft : '--with%s-%s' % ('' if get('I_USE_' + opt.upper(), dft).lower().startswith('y') else 'out', opt)

args = [configure_script]
args += ['--%s=%s' % (d, evald_dirs[d]) for d in param_dirs]
args.append('--disable-option-checking')
args.append(_bool('shared',     'y'))
args.append(_bool('static',     'n'))
args.append(_bool('largefiles', 'y'))
args.append(_bool('valgrind',   'n'))
args.append(_bool('selinux',    'n'))
args.append(_bool('nls',        'y'))
args.append(_with('dmalloc',    'y'))
args += extra_args

execute(args)

