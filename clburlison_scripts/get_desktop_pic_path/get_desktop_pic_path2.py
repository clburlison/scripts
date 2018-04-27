#!/usr/bin/python
from AppKit import NSWorkspace, NSScreen, NSBundle

# Frogor hack https://goo.gl/mvQ7Gw
bundle = NSBundle.mainBundle()
info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
info['LSUIElement'] = '1'

ws = NSWorkspace.sharedWorkspace()
for screen in NSScreen.screens():
    print ws.desktopImageURLForScreen_(screen)