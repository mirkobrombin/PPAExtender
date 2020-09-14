#!/usr/bin/python3
'''
   Copyright 2017 Mirko Brombin (brombinmirko@gmail.com)
   Copyright 2017 Ian Santopietro (ian@system76.com)

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

import gettext
from logging import getLogger

import gi
from gi.repository import Gtk

from . import repo
from .list import List
from .settings import Settings
from .updates import Updates

gi.require_version('Gtk', '3.0')
try:
    from .flatpak import Flatpak
except (ImportError, ValueError):
    Flatpak = False

gettext.bindtextdomain('repoman', '/usr/share/repoman/po')
gettext.textdomain("repoman")
_ = gettext.gettext

class Stack(Gtk.Box):

    def __init__(self, parent):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.parent = parent
        self.log = getLogger('repoman.Stack')
        self.log.debug('Logging established.')
        try:
            self.system_repo = repo.get_system_repo()
            self.log.debug('Got system sources at %s', self.system_repo.filename)
        except:
            self.log.debug("Can't get system repo")
            self.system_repo = None

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)

        self.setting = Settings(self)
        self.stack.add_titled(self.setting, "settings", _("Settings"))
        
        self.updates = Updates(self)
        self.stack.add_titled(self.updates, "updates", _("Updates"))
        
        self.list_all = List(self)
        self.stack.add_titled(self.list_all, "list", _("Extra Sources"))
        
        if Flatpak:
            self.flatpak = Flatpak(self)

        if Flatpak:
            self.stack.add_titled(self.flatpak, "flatpak", _("Flatpak"))

        self.pack_start(self.stack, True, True, 0)
