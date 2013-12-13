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


rm_r_ = rm_r
def rm_r(ps):
    for p in ([ps] if isinstance(ps, str) else ps):
        if os.path.lexists(p):
            rm_r(p)


from fh import *

pkgdir  = evald_dirs['destdir']
pkgname = evald_dirs['pkgname']

i_use_devel      = get('I_USE_DEVEL',      'y').lower().startswith('y')
i_use_emacs      = get('I_USE_EMACS',      'y').lower().startswith('y')
i_use_info       = get('I_USE_INFO',       'y').lower().startswith('y')
i_use_man        = get('I_USE_MAN',        'y').lower().startswith('y')
i_use_man_locale = get('I_USE_MAN_LOCALE', '*')
i_use_doc        = get('I_USE_DOC',        'y').lower().startswith('y')
i_use_locale     = get('I_USE_LOCALE',     '*')
i_use_locale_man = get('I_USE_LOCALE_MAN', 'en')
i_use_license    = get('I_USE_LICENSE',    'y').lower().startswith('y')

includedir   = pkgdir + evald_dirs['includedir']
pkgconfigdir = pkgdir + evald_dirs['pkgconfigdir']
infodir      = pkgdir + evald_dirs['infodir']
mandir       = pkgdir + evald_dirs['mandir']
docdir       = pkgdir + evald_dirs['docdir']
localedir    = pkgdir + evald_dirs['localedir']
licensedir   = pkgdir + evald_dirs['licensedir']

datarootdir = pkgdir + evald_dirs['datarootdir']


if not i_use_devel:
    rm_r(pkgdir + includedir)
    rm_r(pkgdir + pkgconfigdir)

if not i_use_emacs:
    rm_r(pkgdir + datarootdir + '/emacs')

if not i_use_info:
    rm_r(pkgdir + infodir)
else:
    rm(pkgdir + infodir + '/dir')

if not i_use_man:
    rm_r(pkgdir + mandir)
else:
    _man = pkgdir + mandir
    _en = _man + os.sep + 'en'
    if not os.path.lexists(_en):
        mkdir_p(_en)
        mv(path('%s/man?/' % path_escape(_man)), _en)
    filter_locale(i_use_man_locale, pkgdir, None, mandir)
    _lang = _man + os.sep + i_use_locale_man
    if os.path.lexists(_lang):
        mv(os.listdir(_lang), _man)
        rmdir(_lang)
    if len(os.listdir(_man)) == 0:
        rmdir(_man)

if not i_use_doc:
    rm_r(pkgdir + docdir)

filter_locale(i_use_locale, pkgdir, None, localedir)

if not i_use_license:
    _dir = '%s%s%s' % (i_use_license, os.sep, pkgname)
    if os.path.lexists(_dir):
        if os.path.islink(_dir):
            rm(_dir)
        else:
            rm_r(_dir)


if os.path.lexists(datarootdir) and os.path.isdir(datarootdir):
    if len(os.listdir(datarootdir)) == 0:
        rmdir(_dir)

