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


fhconf = os.getenv('SYSCONFDIR', '/etc') + '/fh.conf'
if not (os.path.exists(fhconf) and os.path.isfile(fhconf)):
    fhconf = '/fh.conf'

dirs = {'destdir'        : '/install_intermediate', # in case you forget to specify it
        'user_home'      : os.getenv('HOME'), # syntactical sugar
        'prefix'         : '/usr',
        'exec_prefix'    : '{prefix}',

        'var_prefix'     : '{root_prefix}',
        'root_prefix'    : '',
        'usr_prefix'     : '/usr',
        'local_prefix'   : '{usr_prefix}{local_infix}',
        
        'local_infix'    : '/local',
        'games_infix'    : '/games',
        
        'bin'            : '/bin',
        'sbin'           : '/sbin',
        'libexec'        : '/libexec',
        'sysconf'        : '/etc',
        'com'            : '/com',
        'var'            : '/var',
        'lib'            : '/lib',
        'include'        : '/include',
        'data'           : '/share',
        'proc'           : '/proc',
        'sys'            : '/sys',
        'run'            : '/run',
        'tmp'            : '/tmp',
        'srv'            : '/srv',
        'skel'           : '/skel',
        
        'bindir'         : '{exec_prefix}{bin}',
        'sbindir'        : '{exec_prefix}{sbin}',
        'libexecdir'     : '{exec_prefix}{libexec}',
        'sysconfdir'     : '{var_prefix}{sysconf}',
        'sharedstatedir' : '{var_prefix}{com}',
        'localstatedir'  : '{var_prefix}{var}',
        'libdir'         : '{exec_prefix}{lib}',
        'includedir'     : '{prefix}{include}',
        'oldincludedir'  : '/usr/include',
        'datarootdir'    : '{prefix}{share}',
        'datadir'        : '{datarootdir}',
        'infodir'        : '{datarootdir}/info',
        'localedir'      : '{datarootdir}/locale',
        'mandir'         : '{datarootdir}/man',
        'docdir'         : '{prefix}/doc/{pkgname}',
        'htmldir'        : '{docdir}',
        'dvidir'         : '{docdir}',
        'pdfdir'         : '{docdir}',
        'psdir'          : '{docdir}',
        'pkgconfigdir'   : '{libdir}/pkgconfig',
        'apirootdir'     : '',
        'devdir'         : '{apirootdir}',
        'ptsdir'         : '{devdir}/pts',
        'shmdir'         : '{devdir}/shm',
        'procdir'        : '{apirootdir}{proc}',
        'sysdir'         : '{apirootdir}{sys}',
        'rundir'         : '{var_prefix}{run}',
        'tmpdir'         : '{var_prefix}{tmp}',
        'vartmpdir'      : '{localstatedir}{tmp}',
        'srvdir'         : '{var_prefix}{srv}',
        'dbdir'          : '{srvdir}/db',
        'ftpdir'         : '{srvdir}/ftp',
        'httpdir'        : '{srvdir}/http',
        'skeldir'        : '{sysconfdir}{skel}',
        'profiledir'     : '{sysconfdir}/profile.d'
        'appdir'         : '{datarootdir}/applications',
        'changelogdir'   : '{datarootdir}/changelogs',
        'dictdir'        : '{datarootdir}/dict',
        'licensedir'     : '{datarootdir}/licenses',
        'miscdir'        : '{datarootdir}/misc',
        'srcdir'         : '{prefix}/src',
        'rootdir'        : '/root',
        'homedir'        : '/home',
        'mntdir'         : '/mnt',
        'mediadir'       : '/media',
        'cachedir'       : '{localstatedir}/cache',
        'emptydir'       : '{localstatedir}/empty',
        'gamesdir'       : '{localstatedir}/games',
        'statedir'       : '{localstatedir}/lib',
        'lockdir'        : '{localstatedir}/lock',
        'logdir'         : '{localstatedir}/log',
        'maildir'        : '{localstatedir}/mail',
        'spooldir'       : '{localstatedir}/spool',
        'lddir'          : '{sysconfdir}/ld.so.conf.d',
        'opt_infix'      : '/opt/{pkgname}',
        'opt_prefix'     : '/opt/{pkgname}'}


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
        dirs['prefix']         = '{usr_prefix}'
        dirs['exec_prefix']    = '{root_prefix}'
        dirs['var_prefix']     = '{root_prefix}'
    elif arg == '--/usr':
        dirs['prefix']         = '{usr_prefix}'
        dirs['exec_prefix']    = '{usr_prefix}'
        dirs['var_prefix']     = '{root_prefix}'
    elif arg == '--/usr/local':
        dirs['prefix']         = '{local_prefix}'
        dirs['exec_prefix']    = '{local_prefix}'
        dirs['var_prefix']     = '{root_prefix}'
        dirs['localstatedir']  = '{var_prefix}{local_infix}/var'
    elif arg == '--/usr/games':
        dirs['prefix']         = '{usr_prefix}{games_infix}'
        dirs['exec_prefix']    = '{usr_prefix}{games_infix}'
        dirs['var_prefix']     = '{root_prefix}'
    elif arg == '--/usr/local/games':
        dirs['prefix']         = '{local_prefix}{games_infix}'
        dirs['exec_prefix']    = '{local_prefix}{games_infix}'
        dirs['var_prefix']     = '{root_prefix}'
        dirs['localstatedir']  = '{var_prefix}{local_infix}/var'
    elif arg == '--/home':
        dirs['prefix']         = '{user_home}/.local'
        dirs['exec_prefix']    = '{user_home}/.local'
        dirs['var_prefix']     = '{user_home}/.local'
        dirs['sysconfdir']     = '{user_home}/.config'
    elif arg == '--/opt':
        dirs['prefix']         = '{opt_prefix}'
        dirs['exec_prefix']    = '{opt_prefix}'
        dirs['sysconfdir']     = '{var_prefix}/etc{opt_infix}'
        dirs['sharedstatedir'] = '{var_prefix}/com{opt_infix}'
        dirs['localstatedir']  = '{var_prefix}/var{opt_infix}'
    elif arg == '--/home/opt':
        dirs['prefix']         = '{user_home}/.local{opt_prefix}'
        dirs['exec_prefix']    = '{user_home}/.local{opt_prefix}'
        dirs['sysconfdir']     = '{user_home}/.config{opt_infix}'
        dirs['sharedstatedir'] = '{user_home}/.local{var_prefix}/com{opt_infix}'
        dirs['localstatedir']  = '{user_home}/.local{var_prefix}/var{opt_infix}'
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

