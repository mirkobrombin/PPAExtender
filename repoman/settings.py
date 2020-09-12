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

import dbus
import gi
import logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import repo
import gettext
gettext.bindtextdomain('repoman', '/usr/share/repoman/po')
gettext.textdomain("repoman")
_ = gettext.gettext

class Settings(Gtk.Box):
    repo_descriptions = {
        'main': _('Officially supported software'),
        'universe': _('Community-maintained software'),
        'restricted': _('Proprietary drivers for devices'),
        'multiverse': _('Software with Copyright or Legal Restrictions')
    }
    
    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)

        self.system_repo = parent.system_repo
        self.log = logging.getLogger('repoman.Settings')
        self.log.debug('Logging established.')
        self.os_name = repo.get_os_name()
        self.handlers = {}
        self.prev_enabled = False

        self.parent = parent

        self.source_check = self.get_new_switch(
            'source-code',
            _('Include source code')
        )
        self.proposed_check = self.get_new_switch(
            f'{repo.get_os_codename()}-proposed',
            _('Prerelease updates')
        )

        source_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)
        source_box.set_hexpand(True)
        source_label = Gtk.Label.new(_('Include source code'))
        source_label.set_halign(Gtk.Align.START)
        source_box.add(source_label)
        source_switch = Gtk.Switch()
        source_switch.suite = f'{repo.get_os_codename()}-proposed'
        source_switch.set_halign(Gtk.Align.END)

        settings_grid = Gtk.Grid()
        settings_grid.set_margin_left(36)
        settings_grid.set_margin_top(24)
        settings_grid.set_margin_right(36)
        settings_grid.set_margin_bottom(12)
        settings_grid.set_hexpand(True)
        settings_grid.set_halign(Gtk.Align.CENTER)
        self.add(settings_grid)

        sources_title = Gtk.Label(_("Official Sources"))
        sources_title.set_halign(Gtk.Align.START)
        Gtk.StyleContext.add_class(sources_title.get_style_context(), "h2")
        settings_grid.attach(sources_title, 0, 0, 1, 1)

        sources_label = Gtk.Label(_("Official sources are provided by %s and its developers. It's recommended to leave these sources enabled.") % self.os_name)
        sources_label.set_line_wrap(True)
        sources_label.set_justify(Gtk.Justification.FILL)
        sources_label.set_halign(Gtk.Align.START)
        Gtk.StyleContext.add_class(sources_label.get_style_context(), "description")
        settings_grid.attach(sources_label, 0, 1, 1, 1)

        self.checks_grid = Gtk.VBox()
        self.checks_grid.set_margin_left(12)
        self.checks_grid.set_margin_top(24)
        self.checks_grid.set_margin_right(12)
        self.checks_grid.set_margin_bottom(12)
        self.checks_grid.set_spacing(12)
        settings_grid.attach(self.checks_grid, 0, 2, 1, 1)

        developer_options = Gtk.Expander()
        developer_options.set_label(_("Developer Options (Advanced)"))
        settings_grid.attach(developer_options, 0, 3, 1, 1)

        self.developer_grid = Gtk.VBox()
        self.developer_grid.set_margin_left(12)
        self.developer_grid.set_margin_top(12)
        self.developer_grid.set_margin_right(36)
        self.developer_grid.set_margin_bottom(12)
        self.developer_grid.set_spacing(12)
        developer_options.add(self.developer_grid)

        developer_label = Gtk.Label(_("These options are primarily of interest to developers."))
        developer_label.set_line_wrap(True)
        developer_label.set_halign(Gtk.Align.START)
        developer_label.set_margin_start(0)
        self.developer_grid.add(developer_label)
        self.developer_grid.add(self.source_check)
        self.developer_grid.add(self.proposed_check)

        self.create_switches()
        self.switches_sensitive = True
        if not self.system_repo:
            self.switches_sensitive = False

    @property
    def checks_enabled(self):
        """ bool: whether the checks/switches are enabled or not. """
        for checkbox in self.checks_grid.get_children():
            if checkbox.toggle.get_active():
                return True
            else:
                continue
        return False
    
    @property
    def switches_sensitive(self):
        for switchbox in self.checks_grid.get_children():
            if switchbox.get_sensitive():
                return True
            else:
                continue
        return False
    
    @switches_sensitive.setter
    def switches_sensitive(self, sensitive):
        for switchbox in self.checks_grid.get_children():
            switchbox.set_sensitive(sensitive)
        for switchbox in self.developer_grid.get_children():
            switchbox.set_sensitive(sensitive)

    def block_handlers(self):
        for widget in self.handlers:
            if widget.handler_is_connected(self.handlers[widget]):
                widget.handler_block(self.handlers[widget])

    def unblock_handlers(self):
        for widget in self.handlers:
            if widget.handler_is_connected(self.handlers[widget]):
                widget.handler_unblock(self.handlers[widget])
    
    def get_new_switch(self, component, description=None):
        """ Creates a Box with a new switch and a description. 

        If the name of the component matches one of the normal default 
        components, include the description of the component. Otherwise use the
        supplied description (if given) or the name of the component.

        Arguments:
            component (str): The name of a distro component to bind to the switch
            description (str): An optional description to use if the component
                isn't of the predefinied normal sources.
        
        Returns:
            A Gtk.Box with the added switch and label description
        """

        switch = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)
        switch.set_hexpand(True)
        if component in self.repo_descriptions:
            description = self.repo_descriptions[component]

        label_text = component
        if description:
            label_text = f'{description} ({component})'
        label = Gtk.Label.new(label_text)
        label.set_halign(Gtk.Align.START)
        switch.label = label
        switch.add(label)
        toggle = Gtk.Switch()
        toggle.set_halign(Gtk.Align.END)
        toggle.set_hexpand(True)
        toggle.component = component
        switch.toggle = toggle
        switch.add(toggle)

        return switch
    
    def create_switches(self):
        """ Create the grid of switches that control the sources. """
        for switch in self.checks_grid.get_children():
            self.checks_grid.remove(switch)

        for component in self.repo_descriptions:
            switch = self.get_new_switch(component)
            self.checks_grid.add(switch)
        
        if self.system_repo:
            for component in self.system_repo.components:
                if component in self.repo_descriptions:
                    continue
                switch = self.get_new_switch(component)
                self.checks_grid.add(switch)
    
    def set_child_checks_sensitive(self):
        self.source_check.set_sensitive(self.prev_enabled)
        self.proposed_check.set_sensitive(self.prev_enabled)
        try:
            self.parent.updates.set_checks_enabled(self.prev_enabled)
        except AttributeError:
            # In case the updates page hasn't been init'd yet
            pass
    
    def show_source_code(self):
        # (active, inconsistent) = self.ppa.get_source_code_enabled()
        # self.source_check.set_active(active)
        # self.source_check.set_inconsistent(inconsistent)
        pass
    
    def show_proposed(self):
        # (active, inconsistent) = self.ppa.get_child_download_state(self.proposed_check.template)
        # self.proposed_check.set_active(active)
        # self.proposed_check.set_inconsistent(inconsistent)
        pass

    def show_distro(self):
        self.block_handlers()

        for checkbox in self.checks_grid.get_children():
            # (active, inconsistent) = self.ppa.get_comp_download_state(checkbox.comp)
            # checkbox.set_active(active)
            # checkbox.set_inconsistent(inconsistent)
            pass

        self.unblock_handlers()
        self.prev_enabled = self.checks_enabled
        self.set_child_checks_sensitive()
        return 0

    def on_component_toggled(self, checkbutton, comp):
        enabled = checkbutton.get_active()
        try:
            # self.ppa.set_comp_enabled(comp, enabled)
            pass
        except dbus.exceptions.DBusException:
            # self.show_distro()
            pass
        
        if self.checks_enabled != self.prev_enabled and self.prev_enabled:
            self.parent.updates.show_updates()
            self.show_proposed()
            self.show_source_code()
        
        if 'multiverse' in checkbutton.get_label():
            self.show_distro()
        
        self.prev_enabled = self.checks_enabled
        self.set_child_checks_sensitive()
        return 0

    def on_source_check_toggled(self, checkbutton):
        enabled = checkbutton.get_active()
        try:
            # self.ppa.set_source_code_enabled(enabled)
            pass
        except dbus.exceptions.DBusException:
            # self.show_distro()
            pass

        return 0

    def on_proposed_check_toggled(self, checkbutton, comp):
        enabled = checkbutton.get_active()
        try:
            # self.ppa.set_child_enabled(comp.name, enabled)
            pass
        except dbus.exceptions.DBusException:
            # self.show_distro()
            pass

        return 0
    