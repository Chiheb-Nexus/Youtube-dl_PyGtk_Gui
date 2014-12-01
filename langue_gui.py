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
############################# Languages ########################################

__author__ = 'nexus'


ui_fr = ["Entrez l'URL de la vidéo Youtube", "http://www.youtube.com/La_Video", "Vidéo", "Basse",
         "Haute", "Qualité", "Choisir la destination", "Télécharger", "Stopper", "Effacer le log",
          "Fichier", "Quitter", "Aide", "À propos", "Bug", "Vous voulez vraiment quitter ?",
         "Pour réporter un Bug ou pous plus d'information", "Visitez", "Enter une format valide", "Télécharger",
         "La version de youtube-dl installée est : "]
ui_an = ["Enter Youtube video URL", "http://www.youtube.com/Put_Your_Video", "Video", "Bad",
         "High", "Quality", "Choose destination", "Download", "Stop", "Clear log", "File",
         "Quit", "Help", "About", "Bug", "You really want to leave ?",
          "To report Bug or for more information :", "Visit", "Enter a valid video format", "Download", ""
          "youtube-dl installed version is : "]

from langue_gui import *
from gi.repository import Gtk, GLib, GdkPixbuf, Gdk

class LangueGui(Gtk.Window):
    """
    Class choose language
    """
    def __init__(self):
        """
        initialize language window
        """
        Gtk.Window.__init__(self, title="Choose language Gui")
        self.set_resizable(False)
        self.set_size_request(300, 200)
        self.set_position(Gtk.WindowPosition.CENTER)
        vbox = Gtk.VBox()
        self.add(vbox)
        hbox = Gtk.HBox()
        vbox.pack_start(hbox,True,True,0)

        LangueGui.status = ""
        
        image1 = Gtk.Image()
        image1.set_from_file("images/fr.png")
        self.fr = Gtk.ToggleButton()
        self.fr.set_image(image1)
        
        image = Gtk.Image()
        image.set_from_file("images/ang.png")
        self.ang = Gtk.ToggleButton()
        self.ang.set_image(image)

        hbox.pack_start(self.fr, True, True, 0)
        hbox.pack_start(self.ang, True, True, 0)
        
        
        
        button = Gtk.Button("Ok")
        button.connect("clicked", self.lang)
        vbox.pack_start(button, False, False, 0)
        
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()



    def lang(self, widget):
        """
        :param widget: Button clicked
        :return: ui_an or ui_fr
        """
        if self.fr.get_active():
            
            LangueGui.status = ui_fr
            self.destroy()
        else:
            LangueGui.status = ui_an
            self.destroy()



#### Test ####

if __name__ == '__main__':
    ll = LangueGui()
    ll.connect("destroy", Gtk.main_quit)
    ll.show_all()
    Gtk.main()





