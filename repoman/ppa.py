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
import apt
import threading
from softwareproperties.SoftwareProperties import SoftwareProperties
from aptsources.sourceslist import SourceEntry
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, GLib

GLib.threads_init()

class RemoveThread(threading.Thread):
    cache = apt.Cache()

    def __init__(self, parent, sources_path, ppa, sp):
        threading.Thread.__init__(self)
        self.parent = parent
        self.sources_path = sources_path
        self.ppa = ppa
        self.sp = sp

    def run(self):
        print("Removing PPA %s" % (self.ppa))
        #GObject.idle_add(self.parent.parent.stack.list_all.ppa_liststore.clear)
        self.sp.remove_source(self.ppa, remove_source_code=True)
        self.sp.sourceslist.save()
        self.cache.open()
        self.cache.update()
        self.cache.open(None)
        self.sp.reload_sourceslist()
        isv_list = self.sp.get_isv_sources()
        GObject.idle_add(self.parent.parent.stack.list_all.generate_entries, isv_list)
        GObject.idle_add(self.parent.parent.stack.list_all.view.set_sensitive, True)
        GObject.idle_add(self.parent.parent.hbar.spinner.stop)

class AddThread(threading.Thread):
    cache = apt.Cache()

    def __init__(self, parent, url, sp):
        threading.Thread.__init__(self)
        self.parent = parent
        self.url = url
        self.sp = sp

    def run(self):
        print("Adding PPA %s" % (self.url))
        #GObject.idle_add(self.parent.parent.stack.list_all.ppa_liststore.clear)
        self.sp.add_source_from_line(self.url)
        self.sp.sourceslist.save()
        self.cache.open()
        self.cache.update()
        self.cache.open(None)
        self.sp.reload_sourceslist()
        isv_list = self.sp.get_isv_sources()
        GObject.idle_add(self.parent.parent.parent.stack.list_all.generate_entries, isv_list)
        GObject.idle_add(self.parent.parent.parent.stack.list_all.view.set_sensitive, True)
        GObject.idle_add(self.parent.parent.parent.hbar.spinner.stop)

class ModifyThread(threading.Thread):
    cache = apt.Cache()

    def __init__(self, parent, old_source, new_source, sp):
        threading.Thread.__init__(self)
        self.parent = parent
        self.old_source = old_source
        self.new_source = new_source
        self.sp = sp

    def run(self):
        index = self.sp.sourceslist.list.index(self.old_source)
        file = self.sp.sourceslist.list[index].file
        self.new_source_entry = SourceEntry(self.new_source,file)
        self.sp.sourceslist.list[index] = self.new_source_entry
        self.sp.sourceslist.save()
        self.cache.open()
        self.cache.update()
        self.cache.open(None)
        self.sp.reload_sourceslist()
        isv_list = self.sp.get_isv_sources()
        GObject.idle_add(self.parent.parent.parent.stack.list_all.generate_entries, isv_list)
        GObject.idle_add(self.parent.parent.parent.stack.list_all.view.set_sensitive, True)
        GObject.idle_add(self.parent.parent.parent.hbar.spinner.stop)

# This method need to be improved
class PPA:
    waiting = "Waiting for PPA"
    invalid = "Not a valid PPA"
    valid = "Valid PPA found"
    sources_path = "/etc/apt/sources.list.d/"
    cache = apt.Cache()
    sp = SoftwareProperties()

    def __init__(self, parent):
        self.parent = parent
        self.get_configuration()

    # Returns a list of all 3rd-party software sources.
    def get_isv(self):
        self.sp.reload_sourceslist()
        list = self.sp.get_isv_sources()
        print(list)
        return list

    # Returns the current distro Components.
    def get_distro_sources(self):
        components = self.sp.distro.source_template.components
        return components

    # Returns the current child repos (updates)
    def get_distro_child_repos(self):
        repos = self.sp.distro.source_template.children
        return repos

    # Get whether a component is enabled or not
    def get_comp_download_state(self, comp):
        (active, inconsistent) = self.sp.get_comp_download_state(comp)
        return (active, inconsistent)

    # Get whether a child repo is enabled or not
    def get_child_download_state(self, child):
        (active, inconsistent) = self.sp.get_comp_child_state(child)
        print(child.name + " (" + str(active) + ", " + str(inconsistent) + ")")
        return (active, inconsistent)

    # Get Source Code State
    def get_source_code_enabled(self):
        enabled = self.sp.get_source_code_state()
        if enabled == None:
            return(False, True)
        else:
            return (enabled, False)

    # Enable/Disable a component
    def set_comp_enabled(self, comp, enabled):
        if enabled == True:
            self.sp.enable_component(comp)
        else:
            self.sp.disable_component(comp)
        return 0

    # Enable/Disable a child repo
    def set_child_enabled(self, child, enabled):
        if enabled == True:
            self.sp.enable_child_source(child)
        else:
            self.sp.disable_child_source(child)
        return 0

    # Enable/Disable source code
    def set_source_code_enabled(self, enabled):
        if enabled == True:
            self.sp.enable_source_code_sources()
        elif enabled == False:
            self.sp.disable_source_code_sources()
        return 0

    # Get the current sources configuration
    def get_configuration(self):
        self.enabledDict = {}
        self.update_automation_level = self.sp.get_update_automation_level() #FIXME Doesn't change
        self.release_upgrades_policy = self.sp.get_release_upgrades_policy() #0 on, 2 off
        self.source_code_state = self.sp.get_source_code_state() # Bool

        for comp in self.sp.distro.source_template.components:
            self.enabledDict[comp.name] = self.sp.get_comp_download_state(comp)[0]
        self.main_enabled = self.enabledDict['main']
        self.univ_enabled = self.enabledDict['universe']
        self.rest_enabled = self.enabledDict['restricted']
        self.mult_enabled = self.enabledDict['multiverse']

        for child in self.sp.distro.source_template.children:
            if child.type != 'deb-src':
                self.enabledDict[child.name] = self.sp.get_comp_child_state(child)[0]
        self.secu_enabled = self.enabledDict['artful-security']
        self.recc_enabled = self.enabledDict['artful-updates']
        self.back_enabled = self.enabledDict['artful-backports']
        self.prop_enabled = self.enabledDict['artful-proposed']
        return 0

    def get_line(self, isdisabled, rtype, archs, uri, version, component):
        """Collect all values from the entries and create an apt line"""
        if isdisabled == True:
            disstr = "#"
        else:
            disstr = ""

        if archs == "[arch]":
            archs = ""

        line = "%s%s %s %s %s %s" % (disstr,
                                     rtype,
                                     archs,
                                     uri,
                                     version,
                                     component)
        return line

    # Turn an added deb line into an apt source
    def deb_line_to_source(self, line):
        print(line)
        source = self.sp._find_source_from_string(line)
        return source

    # Modify an existing PPA
    def modify_ppa(self, old_source, disabled, rtype, archs, uri, version, component):
        print("Old source: %s\n" % old_source)
        line = self.get_line(disabled, rtype, archs, uri, version, component)
        print(line)
        self.parent.parent.parent.hbar.spinner.start()
        self.parent.parent.parent.stack.list_all.view.set_sensitive(False)
        ModifyThread(self.parent, old_source, line, self.sp).start()


    # Starts a new thread to add a repository
    def add(self, url):
        self.parent.parent.parent.hbar.spinner.start()
        self.parent.parent.parent.stack.list_all.view.set_sensitive(False)
        AddThread(self.parent, url, self.sp).start()

    # Starts a new thread to remove a repository
    def remove(self, ppa):
        self.parent.parent.hbar.spinner.start()
        self.parent.parent.stack.list_all.view.set_sensitive(False)
        RemoveThread(self.parent, self.sources_path, ppa, self.sp).start()



    def list_all(self):
        sp = SoftwareProperties()
        isv_sources = sp.get_isv_sources()
        source_list = []
        for source in isv_sources:
            if not str(source).startswith("#"):
                source_list.append(str(source))
        return source_list
