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
    import constants
    import ppa
except ImportError:
    import repoman.constants
    import repoman.ppa

class Settings(Gtk.Box):

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)

        self.ppa = ppa.PPA(self)
        self.handlers = {}

        self.parent = parent

        self.checkbutton_source_code = Gtk.CheckButton(label="Include source code")


        settings_grid = Gtk.Grid()
        settings_grid.set_margin_left(12)
        settings_grid.set_margin_top(24)
        settings_grid.set_margin_right(12)
        settings_grid.set_margin_bottom(12)
        settings_grid.set_hexpand(True)
        settings_grid.set_halign(Gtk.Align.CENTER)
        self.add(settings_grid)

        sources_title = Gtk.Label("Official Sources")
        sources_title.set_halign(Gtk.Align.START)
        Gtk.StyleContext.add_class(sources_title.get_style_context(), "h2")
        settings_grid.attach(sources_title, 0, 0, 1, 1)

        sources_label = Gtk.Label("Official sources are those provided by Pop!_OS " +
                                 "and its developers. \nIt's recommended to leave " +
                                 "these sources enabled.")
        sources_label.set_line_wrap(True)
        sources_label.set_halign(Gtk.Align.START)
        settings_grid.attach(sources_label, 0, 1, 1, 1)

        self.checks_grid = Gtk.VBox()
        self.checks_grid.set_margin_left(12)
        self.checks_grid.set_margin_top(24)
        self.checks_grid.set_margin_right(12)
        self.checks_grid.set_margin_bottom(12)
        settings_grid.attach(self.checks_grid, 0, 2, 1, 1)

        developer_options = Gtk.Expander()
        developer_options.set_label("Developer Options (Advanced)")
        settings_grid.attach(developer_options, 0, 3, 1, 1)

        developer_grid = Gtk.Grid()
        developer_grid.set_margin_left(12)
        developer_grid.set_margin_top(24)
        developer_grid.set_margin_right(12)
        developer_grid.set_margin_bottom(12)
        developer_options.add(developer_grid)

        developer_label = Gtk.Label("These options are those which are " +
                                    "primarily of interest to \ndevelopers.")
        developer_label.set_line_wrap(True)
        developer_grid.attach(developer_label, 0, 0, 1, 1)

        self.init_distro()
        self.show_distro()

    def block_handlers(self):
        for widget in self.handlers:
            if widget.handler_is_connected(self.handlers[widget]):
                widget.handler_block(self.handlers[widget])

    def unblock_handlers(self):
        for widget in self.handlers:
            if widget.handler_is_connected(self.handlers[widget]):
                widget.handler_unblock(self.handlers[widget])

    def init_distro(self):

        for checkbutton in self.checks_grid.get_children():
            self.checks_grid.remove(checkbutton)

        distro_comps = self.ppa.get_distro_sources()

        for comp in distro_comps:
            description = comp.description
            if description == 'Non-free drivers':
                description = "Proprietary Drivers for Devices"
            elif description == 'Restricted software':
                description = "Software with Copyright or Legal Restrictions"
            else:
                description = description + " software"

            label = "%s (%s)" % (description, comp.name)
            checkbox = Gtk.CheckButton(label=label)

            checkbox.comp = comp
            self.handlers[checkbox] = checkbox.connect("toggled",
                                                       self.on_component_toggled,
                                                       comp.name)

            self.checks_grid.add(checkbox)
            checkbox.show()
        return 0

    def show_distro(self):
        self.block_handlers()

        for checkbox in self.checks_grid.get_children():
            (active, inconsistent) = self.ppa.get_comp_download_state(checkbox.comp)
            checkbox.set_active(active)
            checkbox.set_inconsistent(inconsistent)

        self.unblock_handlers()

    def on_component_toggled(self, checkbutton, comp):
        if checkbutton.get_active() == True:
            self.ppa.enable_comp(comp)
        else:
            self.ppa.disable_comp(comp)
        return 0
    
