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
from softwareproperties.SoftwareProperties import SoftwareProperties
try:
    import constants as cn
    import ppa as p
except ImportError:
    import repoman.constants as cn
    import repoman.ppa as p

class List(Gtk.ScrolledWindow):

    listiter_count = 0

    def __init__(self, parent):
        self.sp = SoftwareProperties()
        Gtk.ScrolledWindow.__init__(self)
        self.parent = parent
        self.ppa = p.PPA(self)

        self.content_grid = Gtk.Grid()
        self.content_grid.set_margin_top(24)
        self.content_grid.set_margin_left(12)
        self.content_grid.set_margin_right(12)
        self.content_grid.set_margin_bottom(12)
        self.content_grid.set_row_spacing(6)
        self.content_grid.set_hexpand(True)
        self.content_grid.set_vexpand(True)
        self.add(self.content_grid)

        sources_title = Gtk.Label("Extra Sources")
        Gtk.StyleContext.add_class(sources_title.get_style_context(), "h2")
        sources_title.set_halign(Gtk.Align.START)
        self.content_grid.attach(sources_title, 0, 0, 1, 1)

        sources_label = Gtk.Label("These sources are for software provided by " +
                                  "a third party. They may present a security " +
                                  "risk or can cause system instability. " +
                                  "\nOnly add sources that you trust.")
        sources_label.set_line_wrap(True)
        sources_label.set_halign(Gtk.Align.START)
        sources_label.set_justify(Gtk.Justification.FILL)
        sources_label.set_hexpand(True)
        self.content_grid.attach(sources_label, 0, 1, 1, 1)

        list_grid = Gtk.Grid()
        self.content_grid.attach(list_grid, 0, 2, 1, 1)

        self.ppa_liststore = Gtk.ListStore(str, str)
        view = Gtk.TreeView(self.ppa_liststore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Source', renderer, markup=0)
        view.append_column(column)
        view.set_hexpand(True)
        view.set_vexpand(True)
        tree_selection = view.get_selection()
        tree_selection.connect('changed', self.on_row_change)
        list_grid.attach(view, 0, 0, 1, 1)

         # add button
        add_button = Gtk.Button.new_from_icon_name("list-add-symbolic",
                                                   Gtk.IconSize.SMALL_TOOLBAR)
        Gtk.StyleContext.add_class(add_button.get_style_context(),
                                   "image-button")
        add_button.set_tooltip_text("Add New Source")
        add_button.connect("clicked", self.on_add_button_clicked)

        # edit button
        edit_button = Gtk.Button.new_from_icon_name("edit-symbolic",
                                                    Gtk.IconSize.SMALL_TOOLBAR)
        Gtk.StyleContext.add_class(edit_button.get_style_context(),
                                   "image-button")
        edit_button.set_tooltip_text("Modify Selected Source")
        edit_button.connect("clicked", self.on_edit_button_clicked)

        action_bar = Gtk.ActionBar()
        Gtk.StyleContext.add_class(action_bar.get_style_context(),
                                   "inline-toolbar")
        action_bar.add(edit_button)
        action_bar.add(add_button)
        list_grid.attach(action_bar, 0, 1, 1, 1)

        self.generate_entries(self.ppa.get_isv())

    def on_edit_button_clicked(self, widget):
        print("Inline Edit Clicked")

    def on_add_button_clicked(self, widget):
        print("Inline Add Clicked")

    def generate_entries(self, isv_list):
        self.ppa_liststore.clear()

        print(str(self.listiter_count))
        self.listiter_count = self.listiter_count + 1

        for source in isv_list:
            if not str(source).startswith("#"):
                source_pretty = self.sp.render_source(source)
                self.ppa_liststore.insert_with_valuesv(-1,
                                                       [0, 1],
                                                       [source_pretty, str(source)])

    def on_row_change(self, widget):
        (model, pathlist) = widget.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,1)
            self.parent.parent.hbar.ppa_name = value
