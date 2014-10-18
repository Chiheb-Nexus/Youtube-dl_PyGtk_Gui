#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Youtube-dl PyGtk Gui
#  
#  Copyright 2014 Chiheb Nexus
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License.
#  
#  This program is distributed in the hope that it will be useful,
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
############################ Main Gui ##########################################

import os,signal
from gi.repository import Gtk,GLib,GdkPixbuf

class GuiYoutube(Gtk.Window) :
	" Classe principale de la Gui Youtube"
	def __init__(self) : 
		# Constructeur de Gtk.Window pour avoir tous ses options

		Gtk.Window.__init__(self,title="Youtube-dl PyGtk Gui")
		# Taille de la fenêtre par défaut
		self.set_default_size(500,500)
		self.set_icon_from_file("icon.png")
		action_group = Gtk.ActionGroup("Mes actions")
		# Nos 2 menus à déclarer
		self.add_fichier_menu_actions(action_group)
		self.add_aide_menu_actions(action_group)
		self.pid = 0
		

		self.ui_file = os.getcwd() +"/gui_menu.xml"
		uimanager = self.create_ui_manager()
		uimanager.insert_action_group(action_group)
		
		menubar = uimanager.get_widget("/MenuBar")
		vbox = Gtk.VBox()
		self.add(vbox)
		vbox.pack_start(menubar,False,False,0)

		# Création d'un table Grid
		table = Gtk.Table(7,6)

		
		# Label de l'entête
		
		text_1 = Gtk.Label("Veuillez entrer l'URL de la vidéo Youtube")
		table.attach(text_1,0,2,0,1)
		
		# Entrée du lien
		
		self.entree = Gtk.Entry()
		self.entree.set_text("http://www.youtube.com/EXEMPLE")
		table.attach(self.entree,0,2,1,2)
		
		# Label du format
		
		label_format = Gtk.Label("Format : ")
		self.combo = Gtk.ComboBoxText()  # Insertion d'un ComboText
		self.combo.insert(0,"171","WEBM [Audio Basse Qualité]") 
		self.combo.insert(1,"140","M4A [Audio]")  
		self.combo.insert(2,"160","MP4 [Vidéo 144p]")
		self.combo.insert(3,"242","WEBM [Vidéo 240p]")
		self.combo.insert(4,"133","MP4 [Vidéo 240p]")
		self.combo.insert(5,"243","WEBM [Vidéo 360p]")
		self.combo.insert(6,"134","MP4 [Vidéo 360p]")
		self.combo.insert(7,"244","WEBM [Vidéo 480p]")
		self.combo.insert(8,"135","MP4 [Vidéo 480p]")
		self.combo.insert(9,"247","WEBM [Vidéo 720p]")
		self.combo.insert(10,"136","MP4 [Vidéo 720p]")
		self.combo.insert(11,"248","WEBM [Vidéo 1080p]")
		self.combo.insert(12,"137","MP4 [Vidéo 1080p]")
		self.combo.insert(13,"17","3GP [Vidéo 176x144]")
		self.combo.insert(14,"36","3GP [Vidéo 320x240]")
		self.combo.insert(15,"5","FLV [Vidéo 400x240]")
		self.combo.insert(16,"43","WEBM [Vidéo 640x360]")
		self.combo.insert(17,"18","MP4 [Vidéo 640x360]")
		self.combo.insert(18,"22","MP4 [Vidéo 1280x720 Meilleure Qualité]")
		table.attach(label_format,0,1,2,3)
		table.attach(self.combo,1,2,2,3)

		
		
		# Boutton pour choisir la destination
		
		destination = Gtk.Button(label="Choisir destination")
		destination.connect("clicked",self.choix_destination)
		self.label_destination = Gtk.Entry()  # Créer une méthode qui affiche et qui saisie la destination
		self.label_destination.set_text("/home/")
		table.attach(destination,0,1,3,4)
		table.attach(self.label_destination,1,2,3,4)
				
		
		
		# Boutton du téléchargement
		
		self.telecharger = Gtk.Button(label="Télécharger")
		self.telecharger.connect("clicked",self.test_format)
		table.attach(self.telecharger,0,1,4,5)
		
		
		
		# Boutton pour stopper le téléchargement
		
		quite = Gtk.Button(label="Stopper")
		quite.connect("clicked",self.kill)  # Méthode Kill tue le processus
		table.attach(quite,1,2,4,5)
		vbox.pack_start(table,True,True,0)
		
		
		# Création d'un TextView
		self.tw_out = Gtk.TextView()
		# Création d'une ScrolledWindow
		sw = Gtk.ScrolledWindow()
		vbox.pack_start(sw,True,True,0)
		# Ajouter le TextView à ScrolledWindow
		sw.add(self.tw_out)
		# TextView pour afficher les erreurs
		self.tw_err = Gtk.TextView()
		# ScroledWindow pour afficher les erreurs
		
		
		# Ajouter ScrolledWindow à TextView
		
		# Création d'un ProgressBar
		self.progress = Gtk.ProgressBar()
		vbox.pack_start(self.progress,False,True,0)

		
		# Boxe et label à la fin de la fenêtre
		
		self.label_stat = Gtk.Label("Chiheb Nexus | http://www.nexus-coding.blogspot.com")
		vbox.pack_end(self.label_stat,True,True,0)
	
	
    # Mettre à jour la progression de ProgressBar
	def update_progress(self,data=None):
		"Mettre à jour la barre de progression"
		self.progress.pulse()
		return True  # Retourner Vrai
    # Tuer le processus en cours d'éexcution
    # C'est valide sur Linux
    # À tester sur Windows
	def kill(self,widget,data=None):
		"Tuer le processus en cours"
		if self.pid !=0 :
			os.kill(self.pid,signal.SIGTERM)
			self.pid =0
    # Processus principal du téléchargement
	def process(self,widget,data=None):
		"Méthode de téléchargement"
		# changer le chemin de répertoire
		chemin = self.label_destination.get_text()
		os.chdir(chemin)
		# Pour l'instant on a besoin de 2 paramètres
		# Url et Format
		url = self.entree.get_text()
		formats = self.combo.get_active_id()
		# On utlisera youtube-dl pour télécharger la vidéo
		params = ['youtube-dl','-f',formats, url]

		def scroll_to_end(textview):
			i = textview.props.buffer.get_end_iter()
			mark = textview.props.buffer.get_insert()
			textview.props.buffer.place_cursor(i)
			textview.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)
		def write_to_textview(io, condition, tw):
			if condition is GLib.IO_HUP:   # GLib.IO_HUP = Hang UP 
				GLib.source_remove(self.source_id_out)  # Enlever self.source_id_out de la boucle principale
				GLib.source_remove(self.source_id_err)  # Enlever self.source_id_err de la boucle principale
				return False
			line = io.readline()                        # Lire le contenu de io
			tw.props.buffer.insert_at_cursor(line)      # Mettre le contenu de io dans le buffer du TextView (tw)
			scroll_to_end(tw)                           # Le TextView a une barre de défilement
			while Gtk.events_pending():        # Chercher s'il y a un évènement en attente
				Gtk.main_iteration_do(False)   # Bloquer l'itération du programme = False 
			return True
		self.pid, stdin, stdout, stderr = GLib.spawn_async(params,\
			flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,\
			standard_output=True,\
			standard_error=True)    
		      
		      
		io = GLib.IOChannel(stdout) # Création d'une variable qui stock les informations du socket de retour
		err = GLib.IOChannel(stderr) # Création d'une variable qui stock les informations du socket d'erreur
		self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,\
			write_to_textview,self.tw_out,priority=GLib.PRIORITY_HIGH)   
			                                   
		self.source_id_err = err.add_watch(GLib.IO_IN|GLib.IO_HUP,\
			write_to_textview,\
			self.tw_out,\
			priority=GLib.PRIORITY_HIGH)
		timeout_id = GLib.timeout_add(100, self.update_progress) # Mettre à jour la ProgressBar

		def closure_func(pid, status, data):
			GLib.spawn_close_pid(pid)     # Faut fermer GLib.spawn_asyn avec GLib.spawn_close_pid()
			GLib.source_remove(timeout_id) # Enlever timeout_id de la boucle principale
			self.progress.set_fraction(0.0) # retourner le barre de progression à son état initial
			self.pid = 0
		GLib.child_watch_add(self.pid, closure_func, None) # GLib.child_watch_add(pid, function, data=None,
		
                                                                
			
			
	def choix_destination (self,widget) :
		" Choisir un fichier de destination"
		dialog = Gtk.FileChooserDialog("Veuillez choisir un dossier de destination",self,Gtk.FileChooserAction.SELECT_FOLDER,\
		(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,"Valider",Gtk.ResponseType.OK))
		dialog.set_default_size(800,400)
		
		response = dialog.run()
		
		if response == Gtk.ResponseType.OK : 
			self.label_destination.set_text(dialog.get_filename())


			# Réactiver dialog.run() pour choisir à nouveau en cas d'erreur
			# Détruire la fenêtre dialog 
			dialog.destroy()

		if response == Gtk.ResponseType.CANCEL :
			dialog.destroy()	
			
		
		
	def quitter (self,widget) : 
		"Méthode qui affiche une fenêtre de dialog si on quitte le programme"
		dialog = DialogQuit(self)
		response = dialog.run()
		
		if response == Gtk.ResponseType.OK :
			Gtk.main_quit()
		if response == Gtk.ResponseType.CANCEL :
			dialog.destroy()

	def add_fichier_menu_actions(self,action_group) :
		"""Ajouter le menu "Fichier"et ses sous-menus"""
		
		action_filemenu = Gtk.Action("FichierMenu","Fichier",None,None)
		action_group.add_action(action_filemenu)
		
		
		
		action_filequit = Gtk.Action("FichierQuitter","Quitter",None,None,Gtk.STOCK_QUIT)
		action_filequit.connect("activate",self.quitter)
		action_group.add_action(action_filequit)
		
	
	
		
	def add_aide_menu_actions (self,action_group) :
		"""Ajouter le menu "Aide" et ses sous-menus  """
		action_aidemenu = Gtk.Action("AideMenu","Aide",None,None)
		action_group.add_action(action_aidemenu)
		action_aidepropos = Gtk.Action("AideApropos","À propos",None,None,self.propos)
		action_aidepropos.connect("activate",self.propos)
		action_group.add_action(action_aidepropos)
		action_aideplus = Gtk.Action("AidePlus","Plus",None,None,None)
		action_aideplus.connect("activate",self.plus)
		action_group.add_action(action_aideplus)
		
		
	def create_ui_manager (self) : 
		" Création de ui_manager "
		uimanager = Gtk.UIManager()
		uimanager.add_ui_from_file(self.ui_file)  

		return uimanager
		
		
	def propos (self,widget) : 
		" à propos"
		about = Gtk.AboutDialog()
		about.set_program_name("Youtube-dl PyGtk")
		about.set_version("<b>Version :</b> 0.0.2")
		about.set_copyright("Chiheb NeXus© - 2014")
		about.set_comments("Ce programme est une interface graphique crée avec PyGtk3+ basée sur Youtube-dl")
		about.set_website("http://www.nexus-coding.blogspot.com")
		author = ["Chiheb Nexus http://www.nexus-coding.blogspot.com"]
		image = GdkPixbuf.Pixbuf.new_from_file("logo.png")
		about.set_icon_from_file("icon.png")
		about.set_logo(image)
		about.set_authors(author)
		about.set_license(" \
    Youtube-dl PyGtk Gui is a youtube video downloader based on youtube-dl \n \
    Copyright (C) 2014  Chiheb Nexus\n \
    This program is free software: you can redistribute it and/or modify \n\
    it under the terms of the GNU General Public License as published by\n\
    the Free Software Foundation, either version 3 of the License. \n \
    This program is distributed in the hope that it will be useful, \n\
    but WITHOUT ANY WARRANTY; without even the implied warranty of \n\
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n \
    See the GNU General Public License for more details. \n \
    You should have received a copy of the GNU General Public License \n\
    along with this program.  If not, see <http://www.gnu.org/licenses/>.")
		
		about.run()
		about.destroy()

	
	def plus(self,widget) : 
		"Pour plus d'informations"
		info = Gtk.MessageDialog(self,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,\
                                         "Pour réporter un Bug ou pour plus d'informations :")
		info.format_secondary_text(" Veuillez visiter Github : https://github.com/Chiheb-Nexus/Youtube-dl_PyGtk_Gui")
		info.run()
		info.destroy()
		
	def info_user(self,widget) : 
		"Notification de choisir un format valide"
		info = Gtk.MessageDialog(self,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,\
                                         "Veuillez entrer un format vidéo valide")
		info.run()
		info.destroy()
	
	def test_format(self,widget) :
		" Tester la format entrée"
		f = self.combo.get_active_id()
		if f == None :
			self.info_user(self)
		else : 
			self.process(self)
		
	
		
class DialogQuit(Gtk.Dialog) :
	"Classe qui ouvre une fenêtre de dialog avant de quitter"
	def __init__(self,parent) : 
		Gtk.Dialog.__init__(self,"Quitter",parent,0,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,\
                                                             Gtk.STOCK_OK,Gtk.ResponseType.OK))
		self.set_default_size(150,100)
		label = Gtk.Label("Vous voulez vraiment quitter ?\nÊtes vous sûr ?")
		box = self.get_content_area()
		box.add(label)
		self.show_all()

		
		
##### progremme test #####
if __name__ == '__main__' :
	win = GuiYoutube()
	win.connect("delete-event",Gtk.main_quit)
	win.show_all()
	Gtk.main()

