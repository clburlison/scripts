#!/usr/bin/env python
# https://gist.github.com/pudquick/f19567c429a5f0ae047f#file-osx_backdrop-py-L67-L71

from AppKit import NSWorkspace, NSBundle
from SystemConfiguration import SCDynamicStoreCopyConsoleUser
username = (SCDynamicStoreCopyConsoleUser(None, None, None) or [None])[0]
username = [username,""][username in [u"loginwindow", None, u""]]

if username:
    bundle = NSBundle.mainBundle()
    info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
    info['LSUIElement'] = '1'
    # NSWorkspace.sharedWorkspace().openFile_('/Applications/Safari.app')
    NSWorkspace.sharedWorkspace().launchApplication_('/Applications/Safari.app')