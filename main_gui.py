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
############################ Main Gui ##########################################

import os
import getpass
import signal
from langue_gui import *
from version import *
from update import *
from authentification import *
from gi.repository import Gtk, GLib, GdkPixbuf, Gdk


class GuiYoutube(Gtk.Window):
    """
    Principal class of GuiYoutube
    """

    def __init__(self):
        """
        Initial Window
        """
        Gtk.Window.__init__(self, title="Youtube-dl PyGtk Gui")
        # Choose Gui Language
        LangueGui()
        self.l_ui = LangueGui.status
        GuiYoutube.l_ui = LangueGui.status
        if self.l_ui =="" : 
            self.l_ui = ui_an
            GuiYoutube.l_ui = ui_an
            
        #self.set_decorated(0) # remove decoration from window
        self.set_resizable(False)
        self.set_size_request(360, 500)
        #self.set_default_size(500, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_from_file("images/icon.png")
        action_group = Gtk.ActionGroup("Mes actions")

        self.add_fichier_menu_actions(action_group)
        self.add_aide_menu_actions(action_group)
        self.pid = 0

        self.ui_file = os.getcwd() + "/gui_menu.xml"
        uimanager = self.create_ui_manager
        uimanager.insert_action_group(action_group)
        menubar = uimanager.get_widget("/MenuBar")

        vbox = Gtk.VBox(False, 2)
        self.add(vbox)
        vbox.pack_start(menubar, False, False, 0)

        notebook = Gtk.Notebook()
        
        table = Gtk.Table(2, 2, True)
        notebook.append_page(table,Gtk.Label(self.l_ui[19]))


        self.label = Gtk.Label()
        self.label.set_text(self.l_ui[0])
        table.attach(self.label, 0, 2, 0, 1)

        self.entree = Gtk.Entry()
        self.entree.set_text(self.l_ui[1])
        table.attach(self.entree, 0, 2, 1, 2)

        label_format = Gtk.Label("Format : ")
        self.combo = Gtk.ComboBoxText()
        self.combo.insert(0, "171", "WEBM [Audio  "+self.l_ui[3]+" "+self.l_ui[5]+"]")
        self.combo.insert(1, "140", "M4A [Audio]")
        self.combo.insert(2, "160", "MP4 ["+self.l_ui[2]+" 144p]")
        self.combo.insert(3, "242", "WEBM ["+self.l_ui[2]+" 240p]")
        self.combo.insert(4, "133", "MP4 ["+self.l_ui[2]+" 240p]")
        self.combo.insert(5, "243", "WEBM ["+self.l_ui[2]+" 360p]")
        self.combo.insert(6, "134", "MP4 ["+self.l_ui[2]+" 360p]")
        self.combo.insert(7, "244", "WEBM ["+self.l_ui[2]+" 480p]")
        self.combo.insert(8, "135", "MP4 ["+self.l_ui[2]+" 480p]")
        self.combo.insert(9, "247", "WEBM ["+self.l_ui[2]+" 720p]")
        self.combo.insert(10, "136", "MP4 ["+self.l_ui[2]+" 720p]")
        self.combo.insert(11, "248", "WEBM ["+self.l_ui[2]+" 1080p]")
        self.combo.insert(12, "137", "MP4 ["+self.l_ui[2]+" 1080p]")
        self.combo.insert(13, "17", "3GP ["+self.l_ui[2]+" 176x144]")
        self.combo.insert(14, "36", "3GP ["+self.l_ui[2]+" 320x240]")
        self.combo.insert(15, "5", "FLV ["+self.l_ui[2]+" 400x240]")
        self.combo.insert(16, "43", "WEBM ["+self.l_ui[2]+" 640x360]")
        self.combo.insert(17, "18", "MP4 ["+self.l_ui[2]+" 640x360]")
        self.combo.insert(18, "22", "MP4 ["+self.l_ui[2]+" 1280x720 "+self.l_ui[4]+" "+self.l_ui[5]+"]")
        table.attach(label_format, 0, 1, 2, 3)
        table.attach(self.combo, 1, 2, 2, 3)

        destination = Gtk.Button(label=self.l_ui[6])
        destination.connect("clicked", self.choix_destination)
        self.label_destination = Gtk.Entry()
        username = getpass.getuser()
        self.label_destination.set_text("/home/"+username)
        table.attach(destination, 0, 1, 3, 4)
        table.attach(self.label_destination, 1, 2, 3, 4)

        self.telecharger = Gtk.Button(label=self.l_ui[7])
        self.telecharger.connect("clicked", self.test_format,"down")

        table.attach(self.telecharger, 0, 1, 4, 5)
        quite = Gtk.Button(label=self.l_ui[8])
        quite.connect("clicked", self.kill)
        table.attach(quite, 1, 2, 4, 5)
        
        vbox.pack_start(notebook,False,False,0)

        self.tbuffer = Gtk.TextBuffer()
        self.tw_out = Gtk.TextView(buffer=self.tbuffer)
        self.tw_out.set_editable(False)
        sw = Gtk.ScrolledWindow()
        vbox.pack_start(sw, True, True, 0)
        sw.add(self.tw_out)
        self.tw_err = Gtk.TextView()
        self.progress = Gtk.ProgressBar()
        vbox.pack_start(self.progress, False, False, 0)
        clear = Gtk.Button(self.l_ui[9])
        clear.connect("clicked", self.clear_log)
        vbox.pack_start(clear,False,False,0)

        self.label_stat = Gtk.Label("Chiheb Nexus | http://www.nexus-coding.blogspot.com")
        label_version = Gtk.Label()
        try:
            txt = version()
            label_version.set_text(self.l_ui[20]+txt)
        except:
            label_version.set_text("youtube-dl n'est pas installé")

        vbox.pack_end(self.label_stat, False, True, 0)
        vbox.pack_end(label_version, False, True, 0)
        notebook.insert_page(auth(self),Gtk.Label("Authentification"),2)
        notebook.insert_page(update_youtube(self),Gtk.Label("Update"),3)
        

    def clear_log(self, widget):
        """
        Clear log in tw.out
        :param widget: The widget is a TextView 

        """
        self.tbuffer.set_text("")
        self.tw_out.set_buffer(self.tbuffer)

    def update_progress(self):
        """
        Update progress bar
        """
        self.progress.pulse()
        return True

    def kill(self, widget):

        """

        Kill Process by PID in Unix/Linux
        """
        if self.pid != 0:
            os.kill(self.pid, signal.SIGTERM)
            self.pid = 0

    def process(self, widget,operator):

        """
        Download method
        url : Youtube URL
        formats : Video Format
        chemin : Save directory
        params : take url & format contents
        """
        if operator == "down":
            chemin = self.label_destination.get_text()
            os.chdir(chemin)
            url = self.entree.get_text()
            formats = self.combo.get_active_id()
            params = ['youtube-dl', '-f', formats, url]
        if operator == "upd":
            params = ['youtube-dl','-U']
        if operator == "auth":
            url = auth.link_entry.get_text()
            _user_name = auth.user.get_text()
            _user_pass = auth.pwd.get_text()
        if _user_name !="" and _user_pass !="":
            chemin = auth.dest_entry.get_text()
            os.chdir(chemin)
            params = ['youtube-dl','-u',_user_name,'-p',_user_pass,url]
        if _user_pass == "" or _user_pass =="":
            params = ['youtube-dl','-f','mp4',url]


        def scroll_to_end(textview):
            """
            props.buffer :The buffer which is displayed
            props.buffer.get_end_iter() : Returns the end iterator for textview.props.buffer
            props.buffer.place_cursor(i) : Move the cursor to i region
            scroll_to_mark(mark, within_margin, use_align, xalign, yalign) : Scrolls text_view so that mark
                is on the screen in the position indicated by xalign and yalign. An alignment of 0.0 indicates left
                 or top,1.0 indicates right or bottom, 0.5 means center. If use_align is False, the text scrolls
                 the minimal distance to get the mark onscreen, possibly not scrolling at all. The effective screen
                 for purposes of this function is reduced by a margin of size within_margin.
            """
            i = textview.props.buffer.get_end_iter()
            mark = textview.props.buffer.get_insert()
            textview.props.buffer.place_cursor(i)
            textview.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)

        def write_to_textview(io, condition, tw):
            """
            :param io: Input/Output message
            :param condition: Condition to realize the output
            :param tw: TextView
            :return: log message (io & err) in TextView
            err : Output error message
            GLib.spawn_async : Executes a child program asynchronously (your program will not block
                               waiting for the child to exit)
            GLib.IOChannel : A data structure representing an IO Channel
            GLib.IOChannel.add_watch : Adds the IOChannel into the default main loop context with the default priority
            GLib IO Conditions :
              glib.IO_IN : There is data to read
              glib.IO_OUT : Data can be written (without blocking).
              glib.IO_PRI : There is urgent data to read.
              glib.IO_ERR : Error condition.
              glib.IO_HUP : Hung up (the connection has been broken, usually for pipes and sockets).
              glib.IO_NVAL : Invalid request. The file descriptor is not open.
            GLib.source_remove : Use this macro as the return value of a GLib.SourceFunc
                                  to remove the GLib.Source from the main loop.
            Gtk.events_pending : Checks if any events are pending. This can be used to update the GUI
                                 and invoke timeouts etc. while doing some time intensive computation.
            Gtk.main_iteration_do() : Runs a single iteration of the mainloop. If no events are waiting
                                      to be processed GTK+ will block until the next event is noticed.
                                      If you don't want to block look at gtk_main_iteration_do() or check
                                       if any events are pending with gtk_events_pending() first.
            GLib.timeout_add : The glib.timeout_add() function sets a function (specified by callback)
                               to be called at regular intervals (specified by interval, with the default
                               priority, glib.PRIORITY_DEFAULT. Additional arguments to pass to callback
                               can be specified after callback. The idle priority may be specified
                               as a keyword-value pair with the keyword "priority".


            """

            if condition is GLib.IO_HUP:
                GLib.source_remove(self.source_id_out)
                GLib.source_remove(self.source_id_err)
                return False
            line = io.readline()
            tw.props.buffer.insert_at_cursor(line)
            scroll_to_end(tw)
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)
            return True

        self.pid, stdin, stdout, stderr = GLib.spawn_async(params,
                                                           flags=GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                                           standard_output=True,
                                                           standard_error=True)

        io = GLib.IOChannel(stdout)
        err = GLib.IOChannel(stderr)
        self.source_id_out = io.add_watch(GLib.IO_IN | GLib.IO_HUP,
                                          write_to_textview, self.tw_out, priority=GLib.PRIORITY_HIGH)

        self.source_id_err = err.add_watch(GLib.IO_IN | GLib.IO_HUP,
                                           write_to_textview,
                                           self.tw_out,
                                           priority=GLib.PRIORITY_HIGH)
        timeout_id = GLib.timeout_add(100, self.update_progress)

        def closure_func(pid, status, data):
            """
            Close function by PID
            :param pid: Process PID to kill it
            :param status: Process status to kill it
            :param data: return Process data to kill it
            GLib.child_watch_add(...) : Sets a function to be called when the child
                                        indicated by pid exits, at the priority priority
            """
            GLib.spawn_close_pid(pid)
            GLib.source_remove(timeout_id)
            self.progress.set_fraction(0.0)
            self.pid = 0

        GLib.child_watch_add(self.pid, closure_func, None)
        self.clear_log(self.tw_out)


    def choix_destination(self, widget):
        """
        Choose save directory
        :param widget: Widget to call
        """
        dialog = Gtk.FileChooserDialog(self.l_ui[6], self,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Validate", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.label_destination.set_text(dialog.get_filename())
            auth.dest_entry.set_text(dialog.get_filename())
            dialog.destroy()

        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def quitter(self, widget):
        """
        Show a dialog window if user try to kill the GUI
        :param widget: widget to call
        """
        dialog = DialogQuit(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            Gtk.main_quit()
        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def add_fichier_menu_actions(self, action_group):
        """
        Add menu and submenu
        :param action_group: is a Gtk.ActionGroup witch implements Gtk.Buildable
        """

        action_filemenu = Gtk.Action("FichierMenu", self.l_ui[10], None, None)
        action_group.add_action(action_filemenu)
        action_filequit = Gtk.Action("FichierQuitter", self.l_ui[11], None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.quitter)
        action_group.add_action(action_filequit)

    def add_aide_menu_actions(self, action_group):
        """
        Add menu help and his submenu
        Menu : Aide/_À propos + Aide/_Plus
        """
        action_aidemenu = Gtk.Action("AideMenu", self.l_ui[12], None, None)
        action_group.add_action(action_aidemenu)
        action_aidepropos = Gtk.Action("AideApropos", self.l_ui[13], None, None, propos)
        action_aidepropos.connect("activate", propos)
        action_group.add_action(action_aidepropos)
        action_aideplus = Gtk.Action("AidePlus", self.l_ui[14], None, None, None)
        action_aideplus.connect("activate", self.plus)
        action_group.add_action(action_aideplus)

    @property
    def create_ui_manager(self):
        """ Création de ui_manager """
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_file(self.ui_file)
        return uimanager

    def plus(self, widget):
        """Pour plus d'informations
        :param widget: widget to call
        """
        info = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
                                 self.l_ui[16])
        info.format_secondary_text(self.l_ui[17]+' Github : https://github.com/Chiheb-Nexus/Youtube-dl_PyGtk_Gui')
        info.run()
        info.destroy()

    def info_user(self, widget):
        """
        Notification to choose a valid format
        :return : process() or info_user()
        :param widget: widget to call
        """
        info = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, self.l_ui[18])
        info.run()
        info.destroy()

    def test_format(self, widget,operator):
        """
        Test input format
        :param widget: widget to call
        """
        f = self.combo.get_active_id()
        if f:
            self.process(self,operator)
        else:
            self.info_user(self)


def propos(widget):
    """
    About dialog window

    """
    about = Gtk.AboutDialog()
    about.set_program_name("Youtube-dl PyGtk")
    about.set_version("<b>Version :</b> 0.0.5")
    about.set_copyright('Chiheb NeXus© - 2014')
    about.set_comments("This program is a frontend Gui of the popular youtube-dl script created with PyGtk3")
    about.set_website("http://www.nexus-coding.blogspot.com")
    author = ["Chiheb Nexus http://www.nexus-coding.blogspot.com"]
    image = GdkPixbuf.Pixbuf.new_from_file('images/logo.png')
    about.set_icon_from_file("images/icon.png")
    about.set_logo(image)
    about.set_authors(author)
    about.set_license(" \
Youtube-dl PyGtk Gui is a frontend Gui of the popular youtube-dl \n \
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


class DialogQuit(Gtk.Dialog):
    """
    Open a Dialog window when quit button is clicked

    """

    def __init__(self, parent):
        """

        initialize DialogQuit
        """
        Gtk.Dialog.__init__(self, "Quitter", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK,
                                                         Gtk.ResponseType.OK))
        self.set_default_size(300, 300)
        label = Gtk.Label("\n"+GuiYoutube.l_ui[15]+"\n\n\n\n")
        image = Gtk.Image()
        image.set_from_file("images/quit.png")

        box = self.get_content_area()
        box.add(label)
        box.add(image)
        self.show_all()


##### Test Program #####

if __name__ == '__main__':
    win = GuiYoutube()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
