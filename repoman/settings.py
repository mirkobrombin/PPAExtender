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

class Settings(Gtk.Box):

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)

        self.parent = parent

        settings_grid = Gtk.Grid()
        settings_grid.set_margin_left(12)
        settings_grid.set_margin_top(12)
        settings_grid.set_margin_right(12)
        settings_grid.set_margin_bottom(12)
        settings_grid.set_hexpand(True)
        settings_grid.set_halign(Gtk.Align.CENTER)
        self.add(settings_grid)

        sources_title = Gtk.Label("Official Sources")
        sources_title.set_halign(Gtk.Align.START)
        Gtk.StyleContext.add_class(sources_title.get_style_context(), "h1")
        settings_grid.attach(sources_title, 0, 0, 1, 1)

        sources_label = Gtk.Label("Official sources are those provided by Pop!_OS " +
                                 "and its developers. \nIt's recommended to leave " +
                                 "these sources enabled.")
        sources_label.set_line_wrap(True)
        sources_label.set_halign(Gtk.Align.START)
        settings_grid.attach(sources_label, 0, 1, 1, 1)

        checks_grid = Gtk.Grid()
        checks_grid.set_margin_left(12)
        checks_grid.set_margin_top(12)
        checks_grid.set_margin_right(12)
        checks_grid.set_margin_bottom(12)
        settings_grid.attach(checks_grid, 0, 2, 1, 1)

        main_check = Gtk.CheckButton.new_with_label("Officially Supported Software (main)")
        univ_check = Gtk.CheckButton.new_with_label("Community Supported Software (universe)")
        rest_check = Gtk.CheckButton.new_with_label("Proprietary Drivers for Devices (restricted)")
        mult_check = Gtk.CheckButton.new_with_label("Software with Copyright or Legal Restrictions (multiverse)")
        checks_grid.attach(main_check, 0, 0, 1, 1)
        checks_grid.attach(univ_check, 0, 1, 1, 1)
        checks_grid.attach(rest_check, 0, 2, 1, 1)
        checks_grid.attach(mult_check, 0, 3, 1, 1)

        developer_options = Gtk.Expander()
        developer_options.set_label("Developer Options (Advanced)")
        settings_grid.attach(developer_options, 0, 3, 1, 1)

        developer_grid = Gtk.Grid()
        developer_grid.set_margin_left(12)
        developer_grid.set_margin_top(12)
        developer_grid.set_margin_right(12)
        developer_grid.set_margin_bottom(12)
        developer_options.add(developer_grid)

        developer_label = Gtk.Label("These options are those whice are " +
                                    "primarily of interest to developers.")
        developer_label.set_line_wrap(True)
        developer_grid.attach(developer_label, 0, 0, 1, 1)

        source_check = Gtk.CheckButton.new_with_label("Include Source Code")
        developer_grid.attach(source_check, 0, 1, 1, 1)

        proposed_check = Gtk.CheckButton.new_with_label("Proposed Updates (artful-proposed)")
        developer_grid.attach(proposed_check, 0, 2, 1, 1)
