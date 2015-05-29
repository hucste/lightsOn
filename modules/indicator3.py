#!/usr/bin/env python3
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

''' Module AppIndicator for python 3.x '''

import os
import subprocess
import sys

try:
    from gi.repository import AppIndicator3
    HAS_INDICATOR = True
except ImportError:
    print('Cant import AppIndicator')
    HAS_INDICATOR = False

try:
    from gi.repository import Gtk
except ImportError:
    print('Cant import Gtk')


class AppIndicator(object):
    ''' Create an application indicator '''

    def __init__(self):
        # create a menu
        self.menu = Gtk.Menu()

        self.img = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT, None)
        self.img.connect('activate', self.on_item_quit_activate)

        if HAS_INDICATOR:
            self.ind = AppIndicator3.Indicator.new('lightsOn_indicator',
                '', AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            #self.ind.set_attention_icon('indicator-messages-new')
            self.ind.set_icon('preferences-desktop-screensaver')

            self.img.show()

            self.menu.append(self.img)
            self.menu.show()

            self.ind.set_menu(self.menu)

        else:
            self.ind = Gtk.StatusIcon()
            self.ind.connect('popup-menu', self.popup_menu_icon)
            self.ind.set_from_icon_name('preferences-desktop-screensaver')
            self.ind.set_title('LightsOn')
            self.ind.set_visible(True)

    def popup_menu_icon(self, ind, button, time):
        ''' Show menu by popup when clic into icon '''

        pos = Gtk.StatusIcon.position_menu(self.menu, ind)

        self.menu.append(self.img)
        self.menu.popup(None, None, None, pos, button, time)
        self.menu.show_all()

    def on_item_quit_activate(self, widget, data=None):
        ''' Method to quit '''
        # launch script with option stop
        #folder = os.path.dirname(sys.argv[0])
        folder = os.path.dirname(os.path.abspath(sys.argv[0]))
        script = folder + '/lightsOn.sh stop'
        subprocess.call(script, shell=True)

        Gtk.main_quit()

    @staticmethod
    def main():
        ''' Main method '''
        Gtk.main()
        return 0
