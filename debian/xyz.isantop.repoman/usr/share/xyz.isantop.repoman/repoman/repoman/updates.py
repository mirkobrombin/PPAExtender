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

class Updates(Gtk.Box):

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)

        self.parent = parent

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

        checks_grid = Gtk.Grid()
        checks_grid.set_margin_left(12)
        checks_grid.set_margin_top(24)
        checks_grid.set_margin_right(12)
        checks_grid.set_margin_bottom(12)
        updates_grid.attach(checks_grid, 0, 2, 1, 1)

        secu_check = Gtk.CheckButton.new_with_label("Important Security Updates " +
                                                    "(artful-security)")
        recc_check = Gtk.CheckButton.new_with_label("Recommended Updates " +
                                                    "(artful-updates)")
        back_check = Gtk.CheckButton.new_with_label("Backported Updates " +
                                                    "(artful-backports)")
        checks_grid.attach(secu_check, 0, 0, 1, 1)
        checks_grid.attach(recc_check, 0, 1, 1, 1)
        checks_grid.attach(back_check, 0, 2, 1, 1)

        separator = Gtk.HSeparator()
        updates_grid.attach(separator, 0, 3, 1, 1)

        notifications_title = Gtk.Label("Update Notifications")
        notifications_title.set_halign(Gtk.Align.START)
        Gtk.StyleContext.add_class(notifications_title.get_style_context(), "h2")
        updates_grid.attach(notifications_title, 0, 4, 1, 1)

        notifications_label = Gtk.Label("Change how Pop!_OS notifies you " +
                                        "about pending software updates.")
        notifications_label.set_line_wrap(True)
        notifications_label.set_halign(Gtk.Align.CENTER)
        updates_grid.attach(notifications_label, 0, 5, 1, 1)

        noti_grid = Gtk.Grid()
        noti_grid.set_margin_left(12)
        noti_grid.set_margin_top(12)
        noti_grid.set_margin_right(12)
        noti_grid.set_margin_bottom(12)
        updates_grid.attach(noti_grid, 0, 6, 1, 1)

        notify_check = Gtk.CheckButton.new_with_label("Notify about new updates")
        noti_grid.attach(notify_check, 0, 0, 1, 1)


        auto_check = Gtk.CheckButton.new_with_label("Automatically install " +
                                                    "important security updates.")
        noti_grid.attach(auto_check, 0, 1, 1, 1)

        version_check = Gtk.CheckButton.new_with_label("Notify about new versions " +
                                                       "of Pop!_OS")
        noti_grid.attach(version_check, 0, 2, 1, 1)
