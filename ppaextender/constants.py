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
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class App:
    application_id = "com.github.mirkobrombin.ppaextender"
    application_name = "PPA Extender"
    application_description = "Easily manage PPA"
    application_version ="1.0"
    main_url = "https://github.com/mirkobrombin/ppaextender"
    bug_url = "https://github.com/mirkobrombin/ppaextender/issues/labels/bug"
    help_url = "https://github.com/mirkobrombin/Word/issues"
    about_authors = {"Mirko Brombin <brombinmirko@gmail.com>"}
    about_comments = application_description
    about_license_type = Gtk.License.GPL_3_0

class Colors:
    primary_color = "#4c6ea5"
    primary_text_color = "#ebf1f9"
    primary_text_shadow_color = "#172d4f"
