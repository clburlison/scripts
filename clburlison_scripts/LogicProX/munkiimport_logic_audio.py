#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Version 2.0.0
# Author: Clayton Burlison <https://clburlison.com>
#
# Tool to call 'munkiimport' against a set of Logic Pro X audio content pkgs.
#
# You may customize options passed to munkiimport using the variable
# 'MUNKIIMPORT_OPTIONS' defined below. Please note that the following
# options will be added automatically later in the script:
# --nointeractive
#
# Expects a single argument: a folder containing audio content
# packages for Logic Pro X. For example:
#
# ./munkiimport_logic_audio.py path/to/LogicProContent/
#

import logging
import os
import subprocess
import sys

##############################################################
# User variables below
##############################################################

LOGICNAME = 'Logic Pro X'

MUNKIIMPORT_OPTIONS = [
    "--subdirectory", "cte/audiovideo/logicx/audio",
    "--developer", "Apple",
    "--category", "Media",
    "--catalog", "production",
    "--icon", "audio.png",
]

##############################################################
# No more variables below
##############################################################

munki_tool = 'munkiimport'

MUNKI_DIR = '/usr/local/munki'
ESSENTIAL_PKGS = [
    'MAContent10_GarageBandCoreContent2.pkg',
    'MAContent10_LogicCoreContent2Assets.pkg',
    'MAContent10_LogicCoreContent2Presets.pkg',
    'ProAudioCoreContent10.pkg']
UPDATE4 = None
ERROR = 50
WARNING = 40
INFO = 30
VERBOSE = 20
DEBUG = 10


def errorExit(err_string, err_code=1):
    L.log(ERROR, err_string)
    sys.exit(err_code)


class ColorFormatter(logging.Formatter):
    # http://ascii-table.com/ansi-escape-sequences.php
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[0;%dm"
    COLORS = {'DEBUG': MAGENTA,
              'VERBOSE': GREEN,
              'INFO': BLUE,
              'WARNING': YELLOW,
              'ERROR': RED}
    LEVELS = {10: 'DEBUG', 20: 'VERBOSE', 30: 'INFO', 40: 'WARNING', 50: 'ERROR'}

    def __init__(self, use_color=True, fmt="%(message)s"):
        logging.Formatter.__init__(self)
        self.use_color = use_color

    def format(self, record):
        # Code to prepend level name to log message
        # if record.levelno != 40:
        #     message = "%s: %s" % (self.LEVELS[record.levelno], record.getMessage())
        # else:
        #     message = record.getMessage()
        # record.message = message
        record.message = record.getMessage()
        s = self._fmt % record.__dict__
        if self.use_color:
            if record.levelno != 30:
                color = 30 + self.COLORS[self.LEVELS[record.levelno]]
                s = self.COLOR_SEQ % color + s + self.RESET_SEQ
        return s


def pref(name):
    p = {}
    if name in p.keys():
        value = p[name]
    else:
        value = None
    return value


def main():
    if len(sys.argv) < 2:
        sys.exit("""Usage:
  ./munkiimport_logic_audio.py path/to/LogicProContent/
  See script comments and the README for more detail.""")

    PKGS_DIR = sys.argv[1]
    PKGS_DIR = os.path.abspath(PKGS_DIR)

    # setup logging
    global L
    L = logging.getLogger('com.github.munkiimport_logic_audio')
    log_stdout_handler = logging.StreamHandler(stream=sys.stdout)
    L.addHandler(log_stdout_handler)
    # Hardcode the verbosity as we're not using optparse
    L.setLevel(INFO)

    # Simple munki sanity check
    if not os.path.exists('/usr/local/munki'):
        errorExit("No Munki installation could be found. Get it at https://github.com/munki/munki.")

    # Import munki
    sys.path.append(MUNKI_DIR)
    munkiimport_prefs = os.path.expanduser('~/Library/Preferences/com.googlecode.munki.munkiimport.plist')
    if munki_tool:
        if not os.path.exists(munkiimport_prefs):
            errorExit("Your Munki repo seems to not be configured. Run munkiimport --configure first.")
        try:
            import imp
            # munkiimport doesn't end in .py, so we use imp to make it available to the import system
            imp.load_source('munkiimport', os.path.join(MUNKI_DIR, 'munkiimport'))
            import munkiimport
            munkiimport.REPO_PATH = munkiimport.pref('repo_path')
        except ImportError:
            errorExit("There was an error importing munkilib, which is needed for --munkiimport functionality.")
        # rewrite some of munkiimport's function names since they were changed to
        # snake case around 2.6.1:
        # https://github.com/munki/munki/commit/e3948104e869a6a5eb6b440559f4c57144922e71
        try:
            munkiimport.repoAvailable()
        except AttributeError:
            munkiimport.repoAvailable = munkiimport.repo_available
            munkiimport.makePkgInfo = munkiimport.make_pkginfo
            munkiimport.findMatchingPkginfo = munkiimport.find_matching_pkginfo
            munkiimport.makeCatalogs = munkiimport.make_catalogs
        if not munkiimport.repoAvailable():
            errorExit("The Munki repo cannot be located. This tool is not interactive; first ensure the repo is mounted.")

    # Check for '__Downloaded Items'
    valid_loc = os.path.join(PKGS_DIR, '__Downloaded Items')
    if not os.path.isdir(valid_loc):
        errorExit('"__Downloaded Items" not found! Please re-download audio content or ' +
                  'select a valid directory.')

    # Start searching and importing packages
    for root, dirs, files in os.walk(valid_loc):
        for name in files:
            need_to_import = True
            if name.endswith((".pkg")):
                pkg_path = os.path.join(root, name)
                # Do 'exists in repo' checks
                pkginfo = munkiimport.makePkgInfo([pkg_path], False)
                # Check if package has already been imported, lifted from munkiimport
                matchingpkginfo = munkiimport.findMatchingPkginfo(pkginfo)
                if matchingpkginfo:
                    L.log(VERBOSE, "Got a matching pkginfo.")
                    if ('installer_item_hash' in matchingpkginfo and
                        matchingpkginfo['installer_item_hash'] ==
                        pkginfo.get('installer_item_hash')):
                        need_to_import = False
                        L.log(INFO,
                            ("We have an exact match for %s in the repo. Skipping.." % (
                                name)))
                else:
                    need_to_import = True

                if need_to_import:
                    if name in ESSENTIAL_PKGS:
                        UPDATE4 = LOGICNAME
                    elif 'Alchemy' in name:
                        UPDATE4 = 'LogicProX-Alchemy'
                    else:
                        UPDATE4 = 'LogicProX-BaseLoops'
                    L.log(INFO, ("%s is an update_for %s." % (name, UPDATE4)))
                    # Import into Munki Repo
                    cmd = [
                        "/usr/local/munki/munkiimport",
                        "--nointeractive",
                        "--unattended-install",
                        "--subdirectory", MUNKIIMPORT_OPTIONS[0],
                        "--update-for", UPDATE4,
                        ]
                    cmd += MUNKIIMPORT_OPTIONS
                    cmd.append(pkg_path)
                    subprocess.call(cmd)
    munkiimport.makeCatalogs()


if __name__ == '__main__':
    main()
