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

import os
import gi
import webbrowser
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite
try:
    import constants
    import ppa
except ImportError:
    import repoman.constants
    import repoman.ppa

class Updates(Gtk.Box):

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)

        self.parent = parent

        self.ppa = ppa.PPA(self)
        self.handlers = {}

        updates_grid = Gtk.Grid()
        updates_grid.set_margin_left(12)
        updates_grid.set_margin_top(24)
        updates_grid.set_margin_right(12)
        updates_grid.set_margin_bottom(12)
        updates_grid.set_hexpand(True)
        updates_grid.set_halign(Gtk.Align.CENTER)
        self.add(updates_grid)

        updates_title = Gtk.Label("Update Sources")
        updates_title.set_halign(Gtk.Align.START)
        Gtk.StyleContext.add_class(updates_title.get_style_context(), "h2")
        updates_grid.attach(updates_title, 0, 0, 1, 1)

        updates_label = Gtk.Label("These sources control how Pop!_OS will " +
                                  "check for updates. \nIt is recommended to " +
                                  "leave these sources enabled.")
        updates_label.set_line_wrap(True)
        updates_label.set_halign(Gtk.Align.START)
        updates_grid.attach(updates_label, 0, 1, 1, 1)

        self.checks_grid = Gtk.VBox()
        self.checks_grid.set_margin_left(12)
        self.checks_grid.set_margin_top(24)
        self.checks_grid.set_margin_right(12)
        self.checks_grid.set_margin_bottom(12)
        updates_grid.attach(self.checks_grid, 0, 2, 1, 1)

        separator = Gtk.HSeparator()
        updates_grid.attach(separator, 0, 3, 1, 1)

        self.notifications_title = Gtk.Label("Update Notifications")
        self.notifications_title.set_halign(Gtk.Align.START)
        Gtk.StyleContext.add_class(self.notifications_title.get_style_context(), "h2")
        updates_grid.attach(self.notifications_title, 0, 4, 1, 1)

        self.notifications_label = Gtk.Label("Change how Pop!_OS notifies you " +
                                        "about pending software updates.")
        self.notifications_label.set_line_wrap(True)
        self.notifications_label.set_halign(Gtk.Align.CENTER)
        updates_grid.attach(self.notifications_label, 0, 5, 1, 1)

        self.noti_grid = Gtk.Grid()
        self.noti_grid.set_margin_left(12)
        self.noti_grid.set_margin_top(12)
        self.noti_grid.set_margin_right(12)
        self.noti_grid.set_margin_bottom(12)
        updates_grid.attach(self.noti_grid, 0, 6, 1, 1)

        notify_check = Gtk.CheckButton.new_with_label("Notify about new updates")
        self.noti_grid.attach(notify_check, 0, 0, 1, 1)


        auto_check = Gtk.CheckButton.new_with_label("Automatically install " +
                                                    "important security updates.")
        self.noti_grid.attach(auto_check, 0, 1, 1, 1)

        version_check = Gtk.CheckButton.new_with_label("Notify about new versions " +
                                                       "of Pop!_OS")
        self.noti_grid.attach(version_check, 0, 2, 1, 1)

        self.init_updates()
        self.show_updates()

    def block_handlers(self):
        for widget in self.handlers:
            if widget.handler_is_connected(self.handlers[widget]):
                widget.handler_block(self.handlers[widget])

    def unblock_handlers(self):
        for widget in self.handlers:
            if widget.handler_is_connected(self.handlers[widget]):
                widget.handler_unblock(self.handlers[widget])

    def init_updates(self):
        print("init_distro")

        for checkbutton in self.checks_grid.get_children():
            self.checks_grid.remove(checkbutton)

        comp_children = self.ppa.get_distro_child_repos()

        for template in comp_children:
            # Do not show -proposed or source entries here
            if template.type == "deb-src":
                continue
            if "proposed" in template.name:
                continue

            if template.description == "Unsupported Updates":
                description = "Backported Updates"
            else:
                description = template.description

            checkbox = Gtk.CheckButton(label="%s (%s)" % (description,
                                                          template.name))
            checkbox.template = template
            self.handlers[checkbox] = checkbox.connect("toggled",
                                                       self.on_child_toggled,
                                                       template)
            self.checks_grid.add(checkbox)
            checkbox.show()
        return 0

    def show_updates(self):
        self.block_handlers()
        print("show updates")

        for checkbox in self.checks_grid.get_children():
            (active, inconsistent) = self.ppa.get_child_download_state(checkbox.template)
            checkbox.set_active(active)
            checkbox.set_inconsistent(inconsistent)
        self.unblock_handlers()
        return 0

    def on_child_toggled(self, checkbutton, child):
        enabled = checkbutton.get_active()
        self.ppa.set_child_enabled(child, enabled)
