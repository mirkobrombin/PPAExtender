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

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite, GObject
try:
    import constants
    import window
except ImportError:
    import repoman.constants
    import repoman.window

class Application(Granite.Application):

    def do_activate(self):
        self.win = window.Window()
        self.win.set_default_size(700, 400)
        self.win.connect("delete-event", Gtk.main_quit)
        self.win.show_all()
        self.win.stack.updates.noti_grid.hide()
        self.win.stack.updates.notifications_title.hide()
        self.win.stack.updates.notifications_label.hide()

        Gtk.main()

app = Application()

stylesheet = """
    @define-color colorPrimary """+constants.Colors.primary_color+""";
    @define-color textColorPrimary """+constants.Colors.primary_text_color+""";
    @define-color textColorPrimaryShadow """+constants.Colors.primary_text_shadow_color+""";
""";

style_provider = Gtk.CssProvider()
style_provider.load_from_data(bytes(stylesheet.encode()))
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

app.run("", 1)
