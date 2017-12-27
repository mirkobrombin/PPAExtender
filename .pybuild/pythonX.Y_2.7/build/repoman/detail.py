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
    import ppa as p
except ImportError:
    import repoman.constants as cn
    import repoman.ppa as p

class Detail(Gtk.Box):
    status = False

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)
        self.ppa = p.PPA(self)
        self.parent = parent

        self.set_border_width(80)
        #win.resize(800,400)

        self.set_orientation(Gtk.Orientation.VERTICAL)

        title = Gtk.Label("Add a software source")
        title.set_name('Title')
        title.set_justify(Gtk.Justification.CENTER)
        self.add(title)

        description = Gtk.Label("Enter source line (ex: ppa:mirkobrombin/ppa) and press Enter")
        description.set_name('Description')
        description.set_justify(Gtk.Justification.CENTER)
        self.add(description)

        validate = Gtk.Label("Waiting for source")
        self.validate = validate
        validate.set_name('Validate')
        validate.set_justify(Gtk.Justification.CENTER)

        entry_grid = Gtk.Grid()
        self.add(entry_grid)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Enter source line here...")
        entry.connect("key-release-event", self.on_entry_key_release)
        entry.connect("activate", self.on_entry_activate)
        entry.set_hexpand(True)
        entry_grid.attach(entry, 0, 0, 1, 1)

        # Add button
        ppa_add = Gtk.Button("Add")
        ppa_add.connect("clicked", self.on_entry_activate)
        Gtk.StyleContext.add_class(ppa_add.get_style_context(), "suggested-action")
        entry_grid.attach(ppa_add, 1, 0, 1, 1)


        self.add(validate)

    def on_entry_key_release(self, entry, ev, data=None):
        url = entry.get_text()
        self.ppa.validate(url, self.validate)

    def on_entry_activate(self, entry):
        if self.status:
            self.ppa.add()
