#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

''' Script python to Launc Application Indicator for script lightsOn.sh '''

import platform

py_version = platform.python_version_tuple()
python_major = int(py_version[0])

import modules

if python_major == 2:
    from modules import indicator

if python_major == 3:
    from modules import indicator3 as indicator

if __name__ == "__main__":
    APP = indicator.AppIndicator()
    APP.main()
