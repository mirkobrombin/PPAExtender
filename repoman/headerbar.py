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
    import ppa
    from window import EditDialog
    from window import AddDialog
except ImportError:
    import repoman.constants as cn
    import repoman.ppa
    from repoman.window import EditDialog
    from repoman.window import AddDialog

class Headerbar(Gtk.HeaderBar):

    ppa_name = False

    def __init__(self, parent):
        self.ppa = ppa.PPA(self)

        Gtk.HeaderBar.__init__(self)
        self.parent = parent

        self.set_show_close_button(True)
        self.set_has_subtitle(False)

        self.switcher = Gtk.StackSwitcher()
        self.switcher.set_baseline_position(Gtk.BaselinePosition.CENTER)
        self.set_custom_title(self.switcher)

        # spinner
        #self.spinner = Gtk.Spinner()
        #self.grid.attach(self.spinner, 0, 0, 1, 1)

        # add button
        self.add_button = Gtk.Button.new_from_icon_name("list-add-symbolic",
                                                   Gtk.IconSize.SMALL_TOOLBAR)
        Gtk.StyleContext.add_class(self.add_button.get_style_context(),
                                   "image-button")
        self.add_button.set_tooltip_text("Add New Source")
        self.add_button.connect("clicked", self.on_add_button_clicked)
        self.pack_end(self.add_button)

        # edit button
        self.edit_button = Gtk.Button.new_from_icon_name("edit-symbolic",
                                                    Gtk.IconSize.SMALL_TOOLBAR)
        Gtk.StyleContext.add_class(self.edit_button.get_style_context(),
                                   "image-button")
        self.edit_button.set_tooltip_text("Modify Selected Source")
        self.edit_button.connect("clicked", self.on_edit_button_clicked)
        self.pack_start(self.edit_button)

    def on_edit_button_clicked(self, widget):
        #self.ppa.remove(self.ppa_name)
        source_info = self.ppa_name.split(" ")
        rtype = source_info[0]
        uri = source_info[-3]
        version = source_info[-2]
        comp = source_info[-1]
        dialog = EditDialog(self.parent, rtype, uri, version, comp)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The SAVE button was clicked.")
        else:
            print("The modify was canceled.")

        dialog.destroy()

    def on_add_button_clicked(self, widget):
        self.parent.stack.stack.set_visible_child(self.parent.stack.list_all)
        #self.ppa.remove(self.ppa_name)
        dialog = AddDialog(self.parent)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            url = dialog.ppa_entry.get_text()
            self.ppa.add(url)

        dialog.destroy()
