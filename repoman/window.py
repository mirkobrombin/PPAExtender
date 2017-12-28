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
from datetime import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
try:
    import constants as cn
    import headerbar as hb
    import stack as sk
    import ppa
except ImportError:
    import repoman.constants as cn
    import repoman.headerbar as hb
    import repoman.stack as sk
    import repoman.ppa

class Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)

        self.hbar = hb.Headerbar(self)
        self.set_titlebar(self.hbar)

        self.stack = sk.Stack(self)
        self.add(self.stack)

        self.hbar.switcher.set_stack(self.stack.stack)

        self.screen = Gdk.Screen.get_default()
        self.css_provider = Gtk.CssProvider()
        try:
            self.css_provider.load_from_path('style.css')
        except GLib.Error:
            self.css_provider.load_from_path('/usr/local/bin/repoman/style.css')
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(self.screen, self.css_provider,
          Gtk.STYLE_PROVIDER_PRIORITY_USER)

class DeleteDialog(Gtk.Dialog):

    ppa_name = False

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Remove Source", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_REMOVE, Gtk.ResponseType.OK),
                             modal=1, use_header_bar=1)

        content_area = self.get_content_area()

        content_grid = Gtk.Grid()
        content_grid.set_margin_top(24)
        content_grid.set_margin_left(24)
        content_grid.set_margin_right(24)
        content_grid.set_margin_bottom(24)
        content_grid.set_column_spacing(36)
        content_grid.set_row_spacing(12)
        content_area.add(content_grid)

        delete_image = Gtk.Image.new_from_icon_name("dialog-warning-symbolic",
                                                Gtk.IconSize.DIALOG)
        content_grid.attach(delete_image, 0, 0, 1, 2)

        delete_label = Gtk.Label("Are you sure you want to remove this source?")
        Gtk.StyleContext.add_class(delete_label.get_style_context(), "h2")
        content_grid.attach(delete_label, 1, 0, 1, 1)

        delete_explain = Gtk.Label("If you remove this source, you will need " +
                                   "to add it again to continue using it.\n" +
                                   "Any software you've installed from this " +
                                   "source will remain installed.")
        content_grid.attach(delete_explain, 1, 1, 1, 1)

        Gtk.StyleContext.add_class(self.get_widget_for_response(Gtk.ResponseType.OK).get_style_context(),
                                   "destructive-action")

        self.show_all()

class AddDialog(Gtk.Dialog):

    ppa_name = False

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add Source", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_ADD, Gtk.ResponseType.OK),
                             modal=1, use_header_bar=1)

        content_area = self.get_content_area()

        content_grid = Gtk.Grid()
        content_grid.set_margin_top(24)
        content_grid.set_margin_left(12)
        content_grid.set_margin_right(12)
        content_grid.set_margin_bottom(12)
        content_grid.set_row_spacing(6)
        content_grid.set_halign(Gtk.Align.CENTER)
        content_grid.set_hexpand(True)
        content_area.add(content_grid)

        add_title = Gtk.Label("Enter Source Line")
        Gtk.StyleContext.add_class(add_title.get_style_context(), "h2")
        content_grid.attach(add_title, 0, 0, 1, 1)

        add_label = Gtk.Label("e.g. ppa:mirkobrombin/ppa")
        content_grid.attach(add_label, 0, 1, 1, 1)

        self.ppa_entry = Gtk.Entry()
        self.ppa_entry.set_placeholder_text("Source Line")
        self.ppa_entry.set_activates_default(True)
        self.ppa_entry.set_width_chars(50)
        self.ppa_entry.set_margin_top(12)
        content_grid.attach(self.ppa_entry, 0, 2, 1, 1)

        Gtk.StyleContext.add_class(self.get_widget_for_response(Gtk.ResponseType.OK).get_style_context(),
                                   "suggested-action")

        self.show_all()


class EditDialog(Gtk.Dialog):

    ppa_name = False

    def __init__(self, parent, repo_type, repo_uri, repo_version,
                 repo_component):
        Gtk.Dialog.__init__(self, "Modify Source", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_SAVE, Gtk.ResponseType.OK),
                             modal=1, use_header_bar=1)

        self.ppa = ppa.PPA(self)
        self.parent = parent
        self.set_default_size(600, 100)

        content_area = self.get_content_area()

        content_grid = Gtk.Grid()
        content_grid.set_margin_top(24)
        content_grid.set_margin_left(12)
        content_grid.set_margin_right(12)
        content_grid.set_margin_bottom(12)
        content_grid.set_column_spacing(12)
        content_grid.set_row_spacing(6)
        content_grid.set_halign(Gtk.Align.FILL)
        content_grid.set_hexpand(True)
        content_area.add(content_grid)

        type_label = Gtk.Label("Type")
        type_label.set_halign(Gtk.Align.END)
        uri_label = Gtk.Label("URI")
        uri_label.set_halign(Gtk.Align.END)
        version_label = Gtk.Label("Version")
        version_label.set_halign(Gtk.Align.END)
        component_label = Gtk.Label("Component")
        component_label.set_halign(Gtk.Align.END)
        content_grid.attach(type_label, 0, 0, 1, 1)
        content_grid.attach(uri_label, 0, 1, 1, 1)
        content_grid.attach(version_label, 0, 2, 1, 1)
        content_grid.attach(component_label, 0, 3, 1, 1)

        type_box = Gtk.ComboBoxText()
        type_box.append("deb", "Binary")
        type_box.append("deb-src", "Source code")
        type_box.set_active_id(repo_type)
        content_grid.attach(type_box, 1, 0, 1, 1)

        uri_entry = Gtk.Entry()
        uri_entry.set_hexpand(True)
        uri_entry.set_placeholder_text("https://ppa.launchpad.net/...")
        uri_entry.set_text(repo_uri)
        uri_entry.set_activates_default(False)
        uri_entry.set_width_chars(40)
        content_grid.attach(uri_entry, 1, 1, 1, 1)

        version_entry = Gtk.Entry()
        version_entry.set_placeholder_text("artful")
        version_entry.set_text(repo_version)
        version_entry.set_activates_default(False)
        content_grid.attach(version_entry, 1, 2, 1, 1)

        component_entry = Gtk.Entry()
        component_entry.set_placeholder_text("release")
        component_entry.set_text(repo_component)
        component_entry.set_activates_default(False)
        content_grid.attach(component_entry, 1, 3, 1, 1)

        remove_button = Gtk.Button.new_with_label("Remove Source")
        Gtk.StyleContext.add_class(remove_button.get_style_context(),
                                   "destructive-action")
        remove_button.set_margin_top(12)
        remove_button.connect("clicked", self.on_remove_button_clicked)
        content_grid.attach(remove_button, 0, 4, 1, 1)

        Gtk.StyleContext.add_class(self.get_widget_for_response(Gtk.ResponseType.OK).get_style_context(),
                                   "suggested-action")

        self.show_all()

    def on_remove_button_clicked(self, widget):
        print("Remove Clicked")
        dialog = DeleteDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The REMOVE button was clicked.")
            self.ppa.remove(self.parent.hbar.ppa_name)
            dialog.destroy()
            self.destroy()
        else:
            print("The Remove was canceled.")
            dialog.destroy()

        
