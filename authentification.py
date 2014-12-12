#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Youtube-dl PyGtk Gui
# 
# Copyright 2014 Chiheb Nexus
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
################################################################################ 
####################### Youtube-dl authentification ############################

import getpass
from gi.repository import Gtk

def auth(self):
	"""
	Download a video with :	user name & password
	"""

	label = Gtk.Label("User name")
	auth.user = Gtk.Entry()
	label2 = Gtk.Label("Password")
	auth.pwd = Gtk.Entry()
	auth.pwd.set_visibility(False)
	link_label = Gtk.Label("Put your link here")
	auth.link_entry = Gtk.Entry()
	auth.link_entry.set_text("http://www.example.com/vid")
	dest_button = Gtk.Button("Choose destination")
	dest_button.connect("clicked",self.choix_destination)
	auth.dest_entry = Gtk.Entry()
	user_path = getpass.getuser()
	auth.dest_entry.set_text("/home/"+user_path)
	valid = Gtk.Button("Download")
	valid.connect("clicked",self.process,"auth")
	stop = Gtk.Button("Stop")
	stop.connect("clicked",self.kill)

	table = Gtk.Table(2,2, True)
	table.attach(Gtk.Label("Download a video with ID & Password"),0,2,0,1)
	table.attach(label,0,1,1,2,Gtk.AttachOptions.SHRINK,Gtk.AttachOptions.SHRINK)
	table.attach(auth.user, 1,2,1,2,Gtk.AttachOptions.SHRINK,Gtk.AttachOptions.SHRINK)
	table.attach(label2, 0,1,2,3,Gtk.AttachOptions.SHRINK,Gtk.AttachOptions.SHRINK)
	table.attach(auth.pwd, 1,2,2,3,Gtk.AttachOptions.SHRINK,Gtk.AttachOptions.SHRINK)
	table.attach(link_label,0,1,3,4,Gtk.AttachOptions.SHRINK,Gtk.AttachOptions.SHRINK)
	table.attach(auth.link_entry,1,2,3,4)
	table.attach(dest_button,0,1,4,5)
	table.attach(auth.dest_entry,1,2,4,5)
	table.attach(valid,0,1,5,6,Gtk.AttachOptions.FILL,Gtk.AttachOptions.FILL)
	table.attach(stop,1,2,5,6,Gtk.AttachOptions.FILL,Gtk.AttachOptions.FILL)

	return table

