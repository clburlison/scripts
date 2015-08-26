#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Based off of work by Tim Sutton here: https://github.com/timsutton/aamporter/blob/master/scripts/munkiimport_cc_installers.py
#
# Tool to call 'munkiimport' against a set of Logic Pro X audio content pkgs.
#
# You may customize options passed to munkiimport using the constant
# 'MUNKIIMPORT_OPTIONS' defined below. Please note that the following
# options will be added automatically later in the script:
# --nointeractive
#
# Expects a single argument: a folder containing audio content pkgs
# for Logic Pro X. For example:
#
# ./munkiimport_logic_audio.py LogicProContent
#
# Packages hierarchy:
# .
# ── Apple Loops
# │   ├── Chillwave
# │   │   └── MAContent10_AppleLoopsChillwave.pkg
# │   ├── Deep House
# │   │   └── MAContent10_AppleLoopsDeepHouse.pkg
# │   ├── Dubstep
# │   │   └── MAContent10_AppleLoopsDubstep.pkg
# │   ├── Electro House
# │   │   └── MAContent10_AppleLoopsElectroHouse.pkg
# │   ├── Hip\ Hop
# │   │   └── MAContent10_AppleLoopsHipHop.pkg
# │   ├── Modern R&B
# │   │   └── MAContent10_AppleLoopsModernRnB.pkg
# │   └── Tech House
# │       └── MAContent10_AppleLoopsTechHouse.pkg
# ├── Bass
# │   └── MAContent10_InstrumentsBass.pkg
#    

import os
import subprocess
import sys

MUNKIIMPORT_OPTIONS = [
    "--subdirectory", "cte/audiovideo/logicx/audio",
    "--developer", "Apple",
    "--category", "Media",
    "--update-for", "Logic Pro X",
    "--catalog", "production",
    "--unattended-install",
]


if len(sys.argv) < 2:
    sys.exit("This script requires a single argument. See the script comments.")

PKGS_DIR = sys.argv[1]
PKGS_DIR = os.path.abspath(PKGS_DIR)

for root, dirs, files in os.walk(PKGS_DIR):
    for name in files:
        if name.endswith((".pkg")):
            pkg_path = os.path.join(root, name)
            cmd = [
                "/usr/local/munki/munkiimport",
                "--nointeractive",
                ]
            cmd += MUNKIIMPORT_OPTIONS
            cmd.append(pkg_path)
            subprocess.call(cmd)
