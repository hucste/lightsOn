#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

''' Script python to display Application Indicator for script lightsOn.sh '''

import os
import platform
import subprocess
import sys

py_version = platform.python_version_tuple()
python_major = int(py_version[0])

if python_major == 2:
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

if python_major == 3:
    try:
        from gi.repository import AppIndicator as appindicator
        #from gi.repository import AppIndicator3 as appindicator
    except ImportError:
        print 'Cant import AppIndicator'

    try:
        from gi.repository import Gdk
    except ImportError:
        print 'Cant import Gdk'

    try:
        from gi.repository import GObject
    except ImportError:
        print 'Cant import GObject'

    try:
        from gi.repository import Gtk
    except ImportError:
        print 'Cant import Gtk'

    try:
        from gi.repository import Pango
    except ImportError:
        print 'Cant import Pango'


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
        #folder = os.getcwd()
        folder = os.path.dirname(sys.argv[0])
        script = folder + '/lightsOn.sh stop'
        subprocess.call(script, shell=True)

        Gtk.main_quit()

    def main(self):
        ''' Main method '''
        Gtk.main()
        return 0

if __name__ == "__main__":
    APP = AppIndicator()
    APP.main()
