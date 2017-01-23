#!/usr/bin/python
"""
I didn't create this but I'm storing it so I can reuse it.
http://stackoverflow.com/a/34967364/4811765
"""
import objc

SSID = "MyWifiNetwork"
PASSWORD = "MyWifiPassword"

objc.loadBundle('CoreWLAN',
                bundle_path='/System/Library/Frameworks/CoreWLAN.framework',
                module_globals=globals())
iface = CWInterface.interface()
networks, err = iface.scanForNetworksWithName_err_(SSID, None)
network = networks.anyObject()
success, err = iface.associateToNetwork_password_err_(network, PASSWORD, None)
