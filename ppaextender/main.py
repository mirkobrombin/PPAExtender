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
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite, GObject
try:
    import constants as cn
    import window as wn
except ImportError:
    import ppaextender.constants as cn
    import ppaextender.window as wn

class Application(Granite.Application):

    def do_activate(self):
        self.win = wn.Window()
        self.win.set_default_size(600, 600) 
        self.win.connect("delete-event", Gtk.main_quit)
        self.win.show_all()
        self.win.hbar.back.hide()
        self.win.hbar.trash.hide()

        Gtk.main()

app = Application()

stylesheet = """
    @define-color colorPrimary """+cn.Colors.primary_color+""";
    @define-color textColorPrimary """+cn.Colors.primary_text_color+""";
    @define-color textColorPrimaryShadow """+cn.Colors.primary_text_shadow_color+""";
""";

style_provider = Gtk.CssProvider()
style_provider.load_from_data(bytes(stylesheet.encode()))
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

app.run("", 1)
