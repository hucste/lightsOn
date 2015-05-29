#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

''' Modules AppIndicator for python 2.x '''

import os
import subprocess
import sys

try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    print 'Cant import pygtk'

try:
    import gtk as Gtk
except ImportError:
    print 'Cant import gtk'

try:
    import appindicator
except ImportError:
    print 'Cant import appindicator'


class AppIndicator(object):
    ''' Create an application indicator '''

    def __init__(self):
        self.ind = appindicator.Indicator("lightsOn_indicator",
            "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        #self.ind.set_attention_icon("indicator-messages-new")
        self.ind.set_icon("preferences-desktop-screensaver")

        # create a menu
        self.menu = Gtk.Menu()

        image = Gtk.ImageMenuItem(Gtk.STOCK_QUIT)
        image.connect("activate", self.quit)
        image.show()
        self.menu.append(image)

        self.menu.show()

        self.ind.set_menu(self.menu)

    def quit(self, widget, data=None):
        ''' Method to quit '''
        # launch script with option stop
        #folder = os.path.dirname(sys.argv[0])
        folder = os.path.dirname(os.path.abspath(sys.argv[0]))
        script = folder + '/lightsOn.sh stop'
        subprocess.call(script, shell=True)

        Gtk.main_quit()

    def main(self):
        ''' Main method '''
        Gtk.main()
        return 0
