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
from softwareproperties.SoftwareProperties import SoftwareProperties
try:
    import constants as cn
    import ppa as p
except ImportError:
    import repoman.constants as cn
    import repoman.ppa as p

class List(Gtk.ScrolledWindow):

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

        self.generate_entries()

    def generate_entries(self, update=False):
        isv_list = self.sp.get_isv_sources()
        source_list = []
        if update == False:
            self.ppa_model = Gtk.ListStore(str, str)

        for source in isv_list:
            if not str(source).startswith("#"):
                source_pretty = self.sp.render_source(source)
                self.ppa_model.insert_with_valuesv(-1,
                                                   [0, 1],
                                                   [source_pretty, str(source)])
        self.ppa_s_sort = Gtk.TreeModelSort(model=self.ppa_model)
        self.treeview = Gtk.TreeView.new_with_model(self.ppa_s_sort)
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        tree_selection = self.treeview.get_selection()
        tree_selection.connect('changed', self.on_row_change)
        for i, column_title in enumerate(["Name"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, markup=i)
            self.treeview.append_column(column)
        self.content_grid.attach(self.treeview, 0, 2, 1, 1)

    def on_row_change(self, widget):
        (model, pathlist) = widget.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,1)
            print(value)
            self.parent.parent.hbar.ppa_name = value
