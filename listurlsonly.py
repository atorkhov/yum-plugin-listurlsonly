#!/usr/bin/python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright (C) 2010 Alexey Torkhov <atorkhov@gmail.com>

from yum.plugins import PluginYumExit, TYPE_INTERACTIVE

requires_api_version = '2.1'
plugin_type = (TYPE_INTERACTIVE,)

def config_hook(conduit):
    parser = conduit.getOptParser()
    if hasattr(parser, 'plugin_option_group'):
        parser = parser.plugin_option_group

    parser.add_option('', '--listurlsonly', dest='urlsonly', action='store_true',
           default=False, help="don't update, just list urls")

def predownload_hook(conduit):
    opts, commands = conduit.getCmdLine()
    if not opts.urlsonly:
        return

    # Fetch a listing of repositories
    repolist = conduit.getRepos()

    # Fetch a listing of packages to download
    pkglist = conduit.getDownloadPackages()

    # Setup a queue of packages to download
    for pkg in pkglist :
        rid = pkg.repoid
        url = repolist.getRepo(rid).urls[0]
        remote = url + pkg.relativepath

        # Check if local package has already downloaded
        if pkg.verifyLocalPkg() :
            continue
 
        print remote

    raise PluginYumExit('exiting because --listurlsonly specified')
