#!/usr/bin/python

from Foundation import NSAppleScript, NSBundle

# Frogor hack https://goo.gl/mvQ7Gw
bundle = NSBundle.mainBundle()
info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
info['LSUIElement'] = '1'

applescript = '''tell application "Finder" \
to get POSIX path of (get desktop picture as alias)'''

app = NSAppleScript.alloc().initWithSource_(applescript)
appresult = app.executeAndReturnError_(None)
if appresult[0]:
    print("User is currently using:")
    print(appresult[0].data())
else:
    print("User is using the default desktop picture")
