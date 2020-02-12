#!/usr/bin/python3
'''
   Copyright 2020 Ian Santopietro (ian@system76.com)

   This file is part of Repoman.

    Repoman is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Repoman is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Repoman.  If not, see <http://www.gnu.org/licenses/>.
'''

import gi
import logging
from os.path import splitext, join
from pathlib import Path
from subprocess import CalledProcessError
from sys import exc_info
from threading import Thread

gi.require_version('Flatpak', '1.0')

from gi.repository import GObject, Gio, Flatpak

# Get User Installation
fp_user_path = join(Path.home(), '.local', 'share', 'flatpak')
fp_user_file = Gio.File.new_for_path(fp_user_path)
fp_user_inst = Flatpak.Installation.new_for_path(fp_user_file, True, None)

# Get System Installation
fp_sys_path = join('var', 'lib', 'flatpak')
fp_sys_file = Gio.File.new_for_path(fp_sys_path)
fp_sys_inst = Flatpak.Installation.new_for_path(fp_sys_file, False, None)

# Functions
def add_remote(name, file):
    """ Adds a remote to the user installation.

    We do user installations by default because that's all that Pop Shop 
    operates on currently. There are maybe plans to allow system-wide remotes, 
    but these aren't yet finalized.

    Arguments:
        name (str): The internal name for the new remote.
        file (Gio.Bytes): The data for the flatpakrepo file to add.
    """
    new_remote = Flatpak.Remote.new_from_file(name, file)
    fp_user_inst.add_remote(new_remote, True, None)

def delete_remote(widget, name, option):
    """ Deletes a remote from the installation of option.

    Arguments:
        widget (Gtk.Widget): A widget to manipulate once the thread is finished.
        name (str): The name of the remote to remove.
        option (str): The installation which the remote is configured on.
    """
    remove_thread = RemoveThread(widget, name, option)
    remove_thread.start()

def get_installation_for_type(option):
    """ Gets the installation for the given type.

    Arguments:
        option (str): The type to get, 'user' or 'system'
    
    Returns:
        The requested :obj:`Flatpak.Installation`
    """
    if option.lower() == 'user':
        return fp_user_inst
    else:
        return fp_sys_inst

def get_remotes(option):
    """ Get a list of remotes.

    Arguments:
        option (str): The type of remotes to get, 'user' or 'system'.
    
    Returns:
        A `list` of :obj:`Flatpak.Remote` objects.
    """
    installation = get_installation_for_type(option)
    return installation.list_remotes()

def get_installed_refs_for_option(option):
    """ Lists all refs installed on the installation for option.

    Arguments:
        option (str): The installation to list, 'user' or 'system.
    
    Returns:
        A `list` of `Flatpak.Remotes` installed on the specified installation.
    """
    installation = get_installation_for_type(option)
    return installation.list_installed_refs()


# Classes
class RemoveThread(Thread):

    def __init__(self, parent, remote, option):
        super().__init__()
        self.option = option
        self.parent = parent
        self.remote = remote
        self.refs = list(self.populate_refs_on_remote(option))

    def populate_refs_on_remote(self, option):
        for ref in get_installed_refs_for_option(option):
            if ref.get_origin() == self.remote:
                yield ref
        
    
    def run(self):
        installation = get_installation_for_type(self.option)
        for ref in self.refs:
            installation.uninstall(
                ref.get_kind(),
                ref.get_name(),
                None,
                ref.get_branch()
            )
        installation.remove_remote(self.remote)
        GObject.idle_add(self.parent.parent.parent.stack.flatpak.generate_entries)
        GObject.idle_add(self.parent.parent.parent.stack.flatpak.view.set_sensitive, True)
        GObject.idle_add(self.parent.parent.parent.hbar.spinner.stop)