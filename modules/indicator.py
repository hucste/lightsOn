#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

#
# # Authors informations
#
# @author: HUC Stéphane
# @email: <devs@stephane-huc.net>
# @url: http://stephane-huc.net
#
# @license : GNU/GPL 3
#

''' Module AppIndicator for python 2.x '''

import os
import subprocess
import sys

try:
    import appindicator
    HAS_INDICATOR = True
except ImportError:
    print 'Cant import appindicator'
    HAS_INDICATOR = False

try:
    import gtk
except ImportError:
    print 'Cant import gtk'

try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    print 'Cant import pygtk'


class AppIndicator(object):
    ''' Create an application indicator '''

    def __init__(self):
        # create a menu
        self.menu = gtk.Menu()

        self.img = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.img.connect('activate', self.on_item_quit_activate)

        if HAS_INDICATOR:
            self.ind = appindicator.Indicator('lightsOn_indicator',
                'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
            self.ind.set_status(appindicator.STATUS_ACTIVE)
            #self.ind.set_attention_icon('indicator-messages-new')
            self.ind.set_icon('preferences-desktop-screensaver')

            self.img.show()

            self.menu.append(self.img)
            self.menu.show()

            self.ind.set_menu(self.menu)

        else:
            self.ind = gtk.StatusIcon()
            self.ind.connect('popup-menu', self.popup_menu_icon)
            self.ind.set_from_icon_name('preferences-desktop-screensaver')
            self.ind.set_title('LightsOn')
            self.ind.set_visible(True)

    def popup_menu_icon(self, ind, button, activate_time):
        ''' Show menu by popup when clic into icon '''

        self.menu.append(self.img)
        self.menu.popup(None, None, gtk.status_icon_position_menu, button,
            activate_time, ind)
        self.menu.show_all()

    def on_item_quit_activate(self, widget, data=None):
        ''' Method to quit '''
        # launch script with option stop
        folder = os.path.dirname(os.path.abspath(sys.argv[0]))
        script = folder + '/lightsOn.sh stop'
        subprocess.call(script, shell=True)

        gtk.main_quit()

    @staticmethod
    def main():
        ''' Main method '''
        gtk.main()
        return 0
