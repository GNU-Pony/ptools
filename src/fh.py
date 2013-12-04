#!/usr/bin/env python3
'''
ptools – software package installations tools

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


fhconf = os.getenv('SYSCONFDIR', '/etc') + '/fh.conf'
if not (os.path.exists(fhconf) and os.path.isfile(fhconf)):
    fhconf = '/fh.conf'

dirs = {'prefix'         : '/usr/local',
        'exec_prefix'    : '{prefix}',
        'var_prefix'     : '{root_prefix}',
        'root_prefix'    : '',
        'usr_prefix'     : '/usr',
        'local_prefix'   : '{usr_prefix}/local',
        'bindir'         : '{exec_prefix}/bin',
        'sbindir'        : '{exec_prefix}/sbin',
        'libexecdir'     : '{exec_prefix}/libexec',
        'sysconfdir'     : '{var_prefix}/etc',
        'sharedstatedir' : '{var_prefix}/com',
        'localstatedir'  : '{var_prefix}/var',
        'libdir'         : '{exec_prefix}/lib',
        'includedir'     : '{prefix}/include',
        'oldincludedir'  : '/usr/include',
        'datarootdir'    : '{prefix}/share',
        'datadir'        : '{datarootdir}',
        'infodir'        : '{datarootdir}/info',
        'localedir'      : '{datarootdir}/locale',
        'mandir'         : '{datarootdir}/man',
        'docdir'         : '{prefix}/doc/{pkgname}',
        'htmldir'        : '{docdir}',
        'dvidir'         : '{docdir}',
        'pdfdir'         : '{docdir}',
        'psdir'          : '{docdir}'}

param_dirs = ('root_prefix', 'usr_prefix', 'local_prefix', 'var_prefix')
param_dirs = list(filter(lambda e : e not in param_dirs, dirs.keys()))
for d in dirs.keys():
    dirs[d] = dirs[d].replace('{', '\1').replace('}', '\1')

if os.path.exists(fhconf) and os.path.isfile(fhconf):
    lines = None
    with open(fhconf, 'r') as file:
        lines = file.read().replace('\t', ' ')
    
    buf = ''
    esc = False
    quote = None
    
    for c in line + '\n':
        if esc:
            buf += c
            esc = False
        elif quote == '\'':
            if c == '\'':
                quote = None
            else:
                buf += c
        elif c == '\\':
            esc = True
        elif c in '{}':
            buf += '\1'
        elif quote == '\"':
            if c == '\"':
                quote = None
            else:
                buf += c
        elif c in '\'\"':
            quote = c
        elif c == '\n':
            buf = buf.split('\0')
            dirs[buf[0]] = buf[1]
            buf = '';
        elif c == ' ':
            if '\0' not in buf:
                buf += '\0'
            if not buf.endswith(' '):
                buf += c
        else:
            buf += c

extra_args = []

dashed = False
option = None
for arg in sys.argv[1:]:
    if option is not None:
        dirs[option] = arg
        option = None
    elif dashed:
        extra_args.append(arg)
    elif arg == '--':
        dashed = True
    elif arg == '--/':
        dirs['prefix']      = '/usr'
        dirs['exec_prefix'] = ''
        dirs['var_prefix']  = ''
    elif arg == '--/usr':
        dirs['prefix']      = '/usr'
        dirs['exec_prefix'] = '/usr'
        dirs['var_prefix']  = ''
    elif arg == '--/usr/local':
        dirs['prefix']      = '/usr/local'
        dirs['exec_prefix'] = '/usr/local'
        dirs['var_prefix']  = ''
    elif arg == '--/home':
        dirs['prefix']      = os.getenv('HOME') + '/.local'
        dirs['exec_prefix'] = os.getenv('HOME') + '/.local'
        dirs['var_prefix']  = os.getenv('HOME') + '/.local'
        dirs['sysconfdir']  = os.getenv('HOME') + '/.config'
    elif arg.startswith('--') and ('=' in arg):
        dirs[arg[2:].split('=')[0]] = '='.join(arg.split('=')[1:])
    elif arg.startswith('--'):
        option = arg[2:]
    else:
        sys.exit(1)
if option is not None:
    sys.exit(1)

evald_dirs = {}
queue = list(dirs.keys())
while len(queue) > 0:
    d = queue[0]
    queue[:] = queue[1:]
    raw = dirs[d]
    evald = ''
    buf = None
    for c in raw:
        if buf is not None:
            if c == '\1':
                if buf in evald_dirs:
                    evald += evald_dirs[buf]
                else:
                    evald = None
                    break
                buf = None
            else:
                buf += c
        elif c == '\1':
            buf = ''
        else:
            evald += c
    if evald is None:
        queue.append(d)
    else:
        evald_dirs[d] = evald

