#!%%PYTHON%%
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License, Version 1.0 only
# (the "License").  You may not use this file except in compliance
# with the License.
#
# You can obtain a copy of the license at OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#
# Copyright (c) 2010, Oracle and/or its affiliates. All rights reserved.
#

import gettext
import os
import glob
import signal
import sys
import getopt
import time
import subprocess
import locale
from os import path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

_  = lambda a : gettext.dgettext("imf-selector", a)

class IMSelector(object):


    IMSCRIPT        = '/etc/X11/xinit/xinitrc.d/0210.im'
    LOCALEDIR       = '/usr/share/locale'
    DATADIR         = '/usr/share/imf-selector'
    XIM_DATA        = {}     # Keep name and script path
    ENABLE_FLAG     = False  # Flag for enabling IM

    def __init__(self):
        super(IMSelector, self).__init__()
        self.__init_ui()
        self.__create_lst()
        self.__mark_cnt_im()

    def __init_ui(self):
        gettext.bindtextdomain("imf-selector", self.LOCALEDIR)
        gettext.bind_textdomain_codeset("imf-selector", "UTF-8")
        self.dlg = Gtk.Dialog(_("Input Method Framework Selector"))
        self.dlg.set_size_request(400,200) 
        self.dlg.set_border_width(5)
        self.dlg.set_type_hint(Gdk.WindowTypeHint.NORMAL)
        self.dlg.connect("delete_event", self.__quit)

        vbox = Gtk.VBox(spacing=7)
        self.dlg.vbox.pack_start(vbox, True, True, 0)

        self.enable_btn = Gtk.CheckButton(_("Enable Input Method Framework"))
        vbox.pack_start(self.enable_btn, False, False, 0)
        self.enable_btn.connect("toggled", self.__toggle_im, None)

        scroll_window = Gtk.ScrolledWindow()
        scroll_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scroll_window, False, False, 0)

        self.tv = Gtk.TreeView() 
        self.lst = Gtk.ListStore(str)
        self.tv.set_model(self.lst)
        tv_clm = Gtk.TreeViewColumn(_("Available Input Method Framework"))
        tv_cl = Gtk.CellRendererText()
        tv_clm.pack_start(tv_cl, True)
        tv_clm.add_attribute(tv_cl, 'text', 0)
        self.tv.append_column(tv_clm)
        scroll_window.add(self.tv) 

        help_btn = Gtk.Button(_("Help"))
        default_btn = Gtk.Button(_("Reset"))
        cancel_btn = Gtk.Button(_("Cancel"))
        ok_btn = Gtk.Button(_("OK"))
        self.dlg.action_area.pack_start(help_btn, True, True, 0) 
        self.dlg.action_area.pack_start(default_btn, True, True, 0)
        self.dlg.action_area.pack_start(cancel_btn, True, True, 0) 
        self.dlg.action_area.pack_start(ok_btn, True, True, 0) 
        help_btn.connect("clicked", self.__launch_help)
        default_btn.connect("clicked", self.__default)
        cancel_btn.connect("clicked", self.__quit)
        ok_btn.connect("clicked", self.__apply)
        cancel_btn.grab_focus()

    def __toggle_im(self, widget=None, data=None):
        if(self.ENABLE_FLAG == True):
            self.__disable_im()
        else:
            self.__enable_im()

    def __launch_help(self, widget=None, data=None):
            os.spawnv(os.P_NOWAIT, "/usr/bin/yelp", ["/usr/bin/yelp", "gnome-help:imf-selector"])

    def __default(self, widget=None, data=None):
        im = self.__exec_script('-default')
        if( im == "None"):
            selection = self.tv.get_selection()
            selection.unselect_all()
            self.__disable_im()
            return None
        name = im.split('|')[0]
        iter = self.lst.get_iter_first()
        while iter:
            value = self.lst.get_value(iter, 0)
            if(name == value):
                selection = self.tv.get_selection()
                selection.select_iter(iter)
                self.__enable_im()
                return
            iter = self.lst.iter_next(iter)
        return None

    def __quit(self, widget=None, data=None):
        Gtk.main_quit()
        return False

    def __disable_im(self):
        self.enable_btn.set_active(False)
        self.tv.set_sensitive(False)
        self.ENABLE_FLAG = False

    def __enable_im(self):
        self.enable_btn.set_active(True)
        self.tv.set_sensitive(True)
        self.ENABLE_FLAG = True

    def __create_lst(self):
        list = self.__exec_script('-list')
        if(list == ""):
            return 0
        for im in list.split('\n'):
            name = im.split('|')[0]
            path = im.split('|')[1]
            self.XIM_DATA[name] = path
            self.lst.append([name])

    def __exec_script(self, opt, arg=""):
        cmd = self.IMSCRIPT + ' ' + opt + ' ' + arg
        try:
            if(os.access(self.IMSCRIPT, os.X_OK)):
                (status, out) = subprocess.getstatusoutput(cmd)
                if(status != 0):
                    msg = _("Following error occured :\n\n") + out
                    self.__show_err_dlg(msg)
                    return False
                return out
            else:
                self.__quit()
        except:
            msg =_("Can not execute configuration script: ") + self.IMSCRIPT
            self.__show_err_dlg(msg)
            return None

    def __mark_cnt_im(self):
        im = self.__exec_script('-get')
        if(im == "None"): 
            selection = self.tv.get_selection()
            selection.unselect_all()
            self.__disable_im()
            return None
        name = im.split('|')[0]
        iter=self.lst.get_iter_first()
        while iter:
            value = self.lst.get_value(iter, 0) 
            if(name == value):
                selection = self.tv.get_selection()
                selection.select_iter(iter)
                self.__enable_im()
                return True
            iter = self.lst.iter_next(iter)
        return None

    def __apply(self, widget=None, data=None):
        selection = self.tv.get_selection()
        iter = selection.get_selected()[1]
        if((not iter) and self.ENABLE_FLAG):
            return
        msg = _("Do you update your configuration ?\n"\
                "This configuration becomes effective "\
                "from next desktop login.")
        dlg = Gtk.MessageDialog(type = Gtk.MessageType.INFO,
                    buttons = Gtk.ButtonsType.YES_NO,
                    message_format = msg)
        id = dlg.run()
        dlg.destroy()
        if id == Gtk.ResponseType.YES:
            if(not self.ENABLE_FLAG):
                if(self.__exec_script('-set') != False):
                    self.__quit()
            else:
                imname = self.lst.get_value(iter, 0)
                if(self.__exec_script('-set', self.XIM_DATA[imname]) != False):
                    self.__quit()
        elif id == Gtk.ResponseType.NO:
            return

    def __unselect_all(self):
        self.__enable_im()
        selection = self.tv.get_selection()
        selection.unselect_all()

    def __show_err_dlg(self, msg):
        dlg = Gtk.MessageDialog(type = Gtk.MessageType.ERROR,
                    buttons = Gtk.ButtonsType.OK,
                    message_format = msg)
        id = dlg.run()
        dlg.destroy()

    def run(self):
        self.dlg.show_all()
        Gtk.main()

    def init_priorui(self, script, engine, imf):
        msg = _("Found Input Method '%s' under '%s' framework on "\
                "system for this locale.\n Do you use this Input Method "\
                "in your desktop ?\n"\
                "This configuration becomes effective "\
                "from next desktop login.") %(engine, imf)
        
        self.priordlg = Gtk.MessageDialog(type = Gtk.MessageType.INFO,
                    buttons = Gtk.ButtonsType.YES_NO,
                    message_format = msg)
        id = self.priordlg.run()
        self.priordlg.destroy()
        if(id == Gtk.ResponseType.YES):
            self.__exec_script('-set', script)
        elif(id == Gtk.ResponseType.NO):
            self.__exec_script('-set', 'IGNORE')
        sys.exit(0)

    def run_prior(self, script, engine, imf):
        self.init_priorui(script, engine, imf)
        Gtk.main()

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:", ["prior="])
    except getopt.error as msg:
        print("%s" %(msg))
        sys.exit(2)

    setup = IMSelector()
    for option, argument in opts:
        if option in ("-p", "--prior"):
            script=argument.split('|')[0]
            engine=argument.split('|')[1]
            imf=argument.split('|')[2]
            setup.run_prior(script, engine, imf)
            sys.exit(0)

    setup.run()
