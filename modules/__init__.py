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

''' Initialize modules '''

import glob, os

dirname = os.path.dirname(os.path.abspath(__file__))

files = glob.glob(dirname + '/*.py')

liste = []

me = os.path.basename(__file__)

for fich in files:
    (path, File) = os.path.split(fich)
    if os.path.isfile(fich) and File != me:
        (name, ext) = os.path.splitext(File)
        if name != '__init__' and not name in liste:
            liste.append(name)

__all__ = liste
