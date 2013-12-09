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

error = 0
_p = dirs['pkgname']

table = [('/bin',                'bindir'),
         ('/sbin',               'sbindir'),
         ('/libexec',            'libexecdir'),
         ('/etc',                'sysconfdir'),
         ('/com',                'sharedstatedir'),
         ('/var',                'localstatedir'),
         ('/lib',                'libdir'),
         ('/include',            'includedir'),
         ('/share',              'datadir'),
         ('/share/info',         'infodir'),
         ('/share/locale',       'localedir'),
         ('/share/man',          'mandir'),
         ('/share/doc/' + _p,    'docdir'),
         ('/doc/' + _p,          'docdir'),
         ('/lib/pkgconfig',      'pkgconfigdir'),
         ('/dev',                'devdir'),
         ('/dev/pts',            'ptsdir'),
         ('/dev/shm',            'shmdir'),
         ('/proc',               'procdir'),
         ('/sys',                'sysdir'),
         ('/run',                'rundir'),
         ('/tmp',                'tmpdir'),
         ('/var/tmp',            'vartmpdir'),
         ('/srv',                'srvdir'),
         ('/srv/db',             'dbdir'),
         ('/srv/ftp',            'ftpdir'),
         ('/srv/http',           'httpdir'),
         ('/etc/skel',           'skeldir'),
         ('/etc/profile.d',      'profiledir'),
         ('/share/applications', 'appdir'),
         ('/share/changelogs',   'changelogdir'),
         ('/share/dict',         'dictdir'),
         ('/share/licenses',     'licensedir'),
         ('/share/misc',         'miscdir'),
         ('/src',                'srcdir'),
         ('/root',               'rootdir'),
         ('/home',               'homedir'),
         ('/mnt',                'mntdir'),
         ('/media',              'mediadir'),
         ('/var/cache',          'cachedir'),
         ('/var/empty',          'emptydir'),
         ('/var/games',          'gamesdir'),
         ('/var/lib',            'statedir'),
         ('/var/lock',           'lockdir'),
         ('/var/log',            'logdir'),
         ('/var/mail',           'maildir'),
         ('/var/spool/mail',     'maildir'),
         ('/var/spool',          'spooldir'),
         ('/etc/ld.so.conf.d',   'lddir')]

table = [(d + '/', k) for (d, k) in table]
table.sort(key = lambda x : -(len(x) - len(x.replace('/', ''))))

for unresolved in extra_args:
    if not unresolved.startswith('/'):
        error = 1
        echo(unresolved)
    else:
        unresolved = os.path.abspath(unresolved) + '/'
        resolved = ''
        
        for (d, key) in table:
            if unresolved.startswith(d):
                unresolved = unresolved[len(d) - 1:]
                resolved += evald_dirs[key]
                break
        
        echo(resolved + unresolved[:-1].replace('/', os.sep))

sys.exit(error)

