#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

''' Module AppIndicator for python 3.x '''

import os
import subprocess
import sys

try:
    from gi.repository import AppIndicator3
except ImportError:
    print('Cant import AppIndicator')

try:
    from gi.repository import Gtk
except ImportError:
    print('Cant import Gtk')


class AppIndicator(object):
    ''' Create an application indicator '''

    def __init__(self):
        self.ind = AppIndicator3.Indicator.new("lightsOn_indicator",
            "", AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        #self.ind.set_attention_icon("indicator-messages-new")
        self.ind.set_icon("preferences-desktop-screensaver")

        # create a menu
        self.menu = Gtk.Menu()

        image = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT, None)
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
