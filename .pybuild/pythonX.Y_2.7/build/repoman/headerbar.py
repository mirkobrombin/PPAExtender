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
    from window import EditDialog
except ImportError:
    import repoman.constants as cn
    import repoman.ppa as p
    from repoman.window import EditDialog

class Headerbar(Gtk.HeaderBar):

    ppa_name = False

    def __init__(self, parent):
        self.ppa = p.PPA(self)

        Gtk.HeaderBar.__init__(self)
        self.parent = parent

        self.set_show_close_button(True)
        self.set_has_subtitle(False)

        self.switcher = Gtk.StackSwitcher()
        self.switcher.set_baseline_position(Gtk.BaselinePosition.CENTER)
        self.set_custom_title(self.switcher)

        # spinner button
        #self.spinner = Gtk.Spinner()
        #self.grid.attach(self.spinner, 0, 0, 1, 1)

        # trash button
        self.trash = Gtk.Button.new_from_icon_name("edit-delete-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        self.trash.connect("clicked", self.on_trash_clicked)
        Gtk.StyleContext.add_class(self.trash.get_style_context(), "destructive-action")
        self.pack_end(self.trash)

    def on_help_clicked(self, widget):
        webbrowser.open_new_tab("https://github.com/mirkobrombin/PPAExtender")

    def on_trash_clicked(self, widget):
        print("Trash Clicked")
        #self.ppa.remove(self.ppa_name)
        dialog = EditDialog(self.parent, "bin",
                            "https://ppa.launchpad.net/system76-dev/archive",
                            "artful",
                            "release")
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The SAVE button was clicked.")
        else:
            print("The modify was canceled.")

        dialog.destroy()

    def hide_trash(self):
        self.trash.hide()

    def show_trash(self):
        self.trash.show()
