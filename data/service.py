#!/usr/bin/python3
'''
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
from gi.repository import GObject, GLib

import dbus
import dbus.service
import dbus.mainloop.glib
import logging
import sys
import time
import os

from softwareproperties.SoftwareProperties import SoftwareProperties
from aptsources.sourceslist import SourceEntry

GLib.threads_init()

class RepomanException(dbus.DBusException):
    _dbus_error_name = 'org.pop-os.repoman.RepomanException'

class PermissionDeniedByPolicy(dbus.DBusException):
    _dbus_error_name = 'org.pop-os.repoman.PermissionDeniedByPolicy'

class AptException(Exception):
    pass

class PPA(dbus.service.Object):
    def __init__(self, conn=None, object_path=None, bus_name=None):
        dbus.service.Object.__init__(self, conn, object_path, bus_name)

        # These are used by PolKit to check privileges
        self.dbus_info = None
        self.polkit = None
        self.enforce_polkit = True
        self.sp = SoftwareProperties()
    
    @dbus.service.method(
        'org.pop-os.repoman.Interface',
        in_signature='s', out_signature='i',
        sender_keyword='sender', connection_keyword='conn'
    )
    def add_repo(self, line, sender=None, conn=None):
        self._check_polkit_privilege(
            sender, conn, 'org.pop-os.repoman.modifysources'
        )
        
