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

    def __init__(self, parent, sources_path, ppa):
        threading.Thread.__init__(self)
        self.parent = parent
        self.sources_path = sources_path
        self.ppa = ppa

    def run(self):
        sp = SoftwareProperties()
        print("Removing PPA %s" % (self.ppa))
        #sp.remove_source(ppa, remove_source_code=True)
        #os.remove(self.sources_path+self.ppa+".list")
        #try:
        #    os.remove(self.sources_path+self.ppa+".list.save")
        #except FileNotFoundError:
        #    pass
        self.cache.open()
        self.cache.update()
        self.cache.open(None)
        self.parent.parent.stack.list_all.ppa_model.clear()
        self.parent.parent.stack.list_all.generate_entries(True)
        self.parent.parent.hbar.trash.set_sensitive(True)

class AddThread(threading.Thread):
    cache = apt.Cache()

    def __init__(self, parent, url):
        threading.Thread.__init__(self)
        self.parent = parent
        self.url = url

    def run(self):
        sp = SoftwareProperties()
        print("Adding PPA %s" % (self.url))
        #sp.add_source_from_line(self.url)
        sp.sourceslist.save()
        self.cache.open()
        self.cache.update()
        self.cache.open(None)
        self.parent.parent.stack.list_all.ppa_model.clear()
        self.parent.parent.stack.list_all.generate_entries(True)

# This method need to be improved
class PPA:
    waiting = "Waiting for PPA"
    invalid = "Not a valid PPA"
    valid = "Valid PPA found"
    sources_path = "/etc/apt/sources.list.d/"
    cache = apt.Cache()

    def __init__(self, parent):
        self.parent = parent

    def add(self, url):
        AddThread(self.parent, url).start()

    def remove(self, ppa):
        RemoveThread(self.parent, self.sources_path, ppa).start()

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
