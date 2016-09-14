#!/usr/bin/python
# This will display a GUI prompt to remove the devices.
from Foundation import NSBundle
BTPP = NSBundle.bundleWithPath_("/System/Library/PreferencePanes/Bluetooth.prefPane")
BluetoothPref = BTPP.classNamed_('DeviceMenuCreator')
pref = BluetoothPref.alloc().init()
result = pref.removeAllDevices()
