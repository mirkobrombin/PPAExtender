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
import apt
import threading
import time
from softwareproperties.SoftwareProperties import SoftwareProperties
import webbrowser
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite, GObject, GLib
try:
    import constants as cn
    from helper import HGtk
except ImportError:
    import repoman.constants as cn
    from repoman.helper import HGtk


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
        GObject.idle_add(self.parent.parent.stack.list_all.ppa_liststore.clear)
        self.sp.remove_source(self.ppa, remove_source_code=True)
        self.sp.sourceslist.save()
        self.cache.open()
        self.cache.update()
        self.cache.open(None)
        self.sp.reload_sourceslist()
        isv_list = self.sp.get_isv_sources()
        GObject.idle_add(self.parent.parent.stack.list_all.generate_entries, isv_list)
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
        GObject.idle_add(self.parent.parent.stack.list_all.ppa_liststore.clear)
        self.sp.add_source_from_line(self.url)
        self.sp.sourceslist.save()
        self.cache.open()
        self.cache.update()
        self.cache.open(None)
        self.sp.reload_sourceslist()
        isv_list = self.sp.get_isv_sources()
        GObject.idle_add(self.parent.parent.stack.list_all.generate_entries, isv_list)
        GObject.idle_add(self.parent.parent.hbar.spinner.stop)

# This method need to be improved
class PPA:
    waiting = "Waiting for PPA"
    invalid = "Not a valid PPA"
    valid = "Valid PPA found"
    sources_path = "/etc/apt/sources.list.d/"
    cache = apt.Cache()
    sp = SoftwareProperties()
    cache = apt.Cache()

    def __init__(self, parent):
        self.parent = parent

    def get_isv(self):
        self.sp.reload_sourceslist()
        list = self.sp.get_isv_sources()
        print(list)
        return list

    def add(self, url):
        self.parent.parent.hbar.spinner.start()
        AddThread(self.parent, url, self.sp).start()

    def remove(self, ppa):
        self.parent.parent.hbar.spinner.start()
        RemoveThread(self.parent, self.sources_path, ppa, self.sp).start()

    def list_all(self):
        sp = SoftwareProperties()
        isv_sources = sp.get_isv_sources()
        source_list = []
        for source in isv_sources:
            if not str(source).startswith("#"):
                source_list.append(str(source))
        return source_list

    def validate(self, url, widget):
        self.url = url
        if url.startswith("ppa:"):
            self.parent.status = True
            widget.set_text(self.valid)
        elif url.startswith("deb"):
            self.parent.status = True
            widget.set_text(self.valid)
        elif url == "":
            self.parent.status = False
            widget.set_text(self.waiting)
        else:
            self.parent.status = False
            widget.set_text(self.invalid)
