#!/usr/bin/python3
'''
   Copyright 2017 Mirko Brombin (brombinmirko@gmail.com)

   This file is part of repoman.

    repoman is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    repoman is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with repoman.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import gi
import webbrowser
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite
try:
    import constants as cn
    import settings2 as st
    import updates as up
    import detail as dt
    import list as ls
except ImportError:
    import repoman.constants as cn
    import repoman.settings2 as st
    import repoman.updates as up
    import repoman.list as ls

class Stack(Gtk.Box):

    # Define variable for GTK global theme
    settings = Gtk.Settings.get_default()

    def __init__(self, parent):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.parent = parent

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)

        self.stack.connect("set_focus_child", self.on_stack_focus_changed)

        self.setting = st.Settings(self)
        self.updates = up.Updates(self)
        self.detail = dt.Detail(self)
        self.list_all = ls.List(self)

        #self.stack.add_titled(self.welcome, "welcome", "Welcome")
        self.stack.add_titled(self.setting, "settings", "Settings")
        self.stack.add_titled(self.updates, "updates", "Updates")
        #self.stack.add_titled(self.detail, "detail", "Detail")
        self.stack.add_titled(self.list_all, "list", "Extra Sources")

        self.pack_start(self.stack, True, True, 0)

    def on_stack_focus_changed(self, widget, extra):
        child = self.stack.get_visible_child_name()
        print(child)
        if child == "list":
            self.parent.hbar.edit_button.show()
            self.parent.hbar.add_button.show()
        else:
            self.parent.hbar.edit_button.hide()
            self.parent.hbar.add_button.hide()
