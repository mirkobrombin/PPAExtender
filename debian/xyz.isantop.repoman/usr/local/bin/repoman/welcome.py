#!/usr/bin/python3
'''
   Copyright 2017 Mirko Brombin (brombinmirko@gmail.com)

   This file is part of PPAExtender.

    PPAExtender is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PPAExtender is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PPAExtender.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import gi
import webbrowser
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite
try:
    import constants as cn
except ImportError:
    import repoman.constants as cn

class Welcome(Gtk.Box):

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)

        self.parent = parent

        # Create welcome widget
        self.welcome = Granite.WidgetsWelcome()
        self.welcome = self.welcome.new(cn.App.application_name, cn.App.application_description)

        # Welcome voices
        self.welcome.append("document-new", "Add PPA", "Add new PPA")
        self.welcome.append("mail-archive", "List PPA", "List your PPA")

        self.welcome.connect("activated", self.on_welcome_activated)

        self.add(self.welcome)

    def on_welcome_activated(self, widget, index):
        self.parent.parent. hbar.toggle_back()
        if index == 0:
            # Add PPA
            self.parent.stack.set_visible_child_name("detail")
        else:
            self.parent.parent. hbar.toggle_trash()
            # List PPA
            self.parent.stack.set_visible_child_name("list")
