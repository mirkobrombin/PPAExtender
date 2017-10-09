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

import gi
import webbrowser
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
try:
    import constants as cn
    import ppa as p
except ImportError:
    import ppaextender.constants as cn
    import ppaextender.ppa as p

class Headerbar(Gtk.HeaderBar):

    ppa_name = False

    def __init__(self, parent):
        self.ppa = p.PPA(self)

        Gtk.HeaderBar.__init__(self)
        self.parent = parent

        self.set_show_close_button(True)
        self.props.title = cn.App.application_name

        # help button
        self.help = Gtk.Button.new_from_icon_name("help-contents", Gtk.IconSize.LARGE_TOOLBAR)
        self.help.connect("clicked", self.on_help_clicked)
        self.pack_end(self.help)

        # trash button
        self.trash = Gtk.Button()
        self.trash = Gtk.Button.new_from_icon_name("edit-delete", Gtk.IconSize.LARGE_TOOLBAR)
        self.trash.connect("clicked", self.on_trash_clicked)
        self.pack_end(self.trash)

        # spinner button
        self.spinner = Gtk.Spinner()
        self.pack_end(self.spinner)

        # back button
        self.back = Gtk.Button("Return")
        self.back.connect("clicked", self.on_back_clicked)
        Gtk.StyleContext.add_class(self.back.get_style_context(), "back-button")
        self.pack_start(self.back)
    
    def on_help_clicked(self, widget):
        webbrowser.open_new_tab("https://github.com/mirkobrombin/PPAExtender")
    
    def on_trash_clicked(self, widget):
        self.ppa.remove(self.ppa_name)
    
    def on_back_clicked(self, widget):
        self.back.hide()
        self.trash.hide()
        self.parent.stack.stack.set_visible_child_name("welcome")

    def toggle_back(self):
        self.back.show()

    def toggle_trash(self):
        self.trash.show()
