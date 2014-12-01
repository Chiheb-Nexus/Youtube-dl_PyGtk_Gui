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
######################### Youtube-dl update ####################################

from version import *
from gi.repository import Gtk

def update_youtube(self):
	"""
	update Youtube-dl
	"""
	table = Gtk.Table()
	v = version()
	msg = Gtk.Label("La version actuelle de youtube-dl installée est : "+v)
	upd = Gtk.Button("Mettre à jour")
	upd.set_size_request(5,5)
	upd.connect("clicked", self.process,"upd")
	buf = Gtk.TextBuffer()
	buf.set_text("En cas d'échec, vous pouvez mettre à jour ou installer youtube-dl via votre terminal :\n \
	- Sous Ubuntu : \n\
	~$ sudo wget https://yt-dl.org/downloads/2013.10.18/youtube-dl -O /usr/local/bin/youtube-dl \n \
	~$ sudo chmod a+x /usr/local/bin/youtube-dl \n\
Puis il suffit d'appuyez sur le bouton mettre à jour pour effectuer la mise à jour de youtube-dl\n\
Pour plus d'informations veuillez visiter ce site web : https://doc.ubuntu-fr.org/youtube-dl")

	text = Gtk.TextView()
	text.set_buffer(buf)
	text.set_editable(False)

	table.attach(msg,0,1,0,1)
	table.attach(upd,0,1,2,3,Gtk.AttachOptions.SHRINK,Gtk.AttachOptions.SHRINK)
	table.attach(text,0,3,3,4)
	
	return table




