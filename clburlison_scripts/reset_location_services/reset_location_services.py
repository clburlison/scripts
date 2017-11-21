#!/usr/bin/python
"""
Reset location services to factory settings. Requires FoundationPlist
which is installed by default with munki - https://github.com/munki/munki/releases.

pinpoint also installs FoundationPlist - https://github.com/clburlison/pinpoint/releases.
"""

import sys
import os
import platform
import subprocess
import objc

from distutils.version import LooseVersion

from Foundation import NSBundle
try:
    sys.path.append('/usr/local/munki/munkilib/')
    sys.path.append('/Library/Application Support/pinpoint/bin')
    import FoundationPlist
except ImportError as error:
    print "Could not find FoundationPlist."
    raise error

# Retrieve system UUID
IOKit_bundle = NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')

functions = [("IOServiceGetMatchingService", b"II@"),
             ("IOServiceMatching", b"@*"),
             ("IORegistryEntryCreateCFProperty", b"@I@@I"),
            ]

objc.loadBundleFunctions(IOKit_bundle, globals(), functions)

def io_key(keyname):
    """Pythonic function to retrieve system info without a subprocess call."""
    return IORegistryEntryCreateCFProperty(IOServiceGetMatchingService(0, \
           IOServiceMatching("IOPlatformExpertDevice")), keyname, None, 0)

def get_hardware_uuid():
    """Returns the system UUID."""
    return io_key("IOPlatformUUID")

def root_check():
    """Check for root access."""
    if not os.geteuid() == 0:
        exit("This must be run with root access.")

def os_vers():
    """Retrieve OS version."""
    return platform.mac_ver()[0]

def os_check():
    """Only supported on 10.8+."""
    if not LooseVersion(os_vers()) >= LooseVersion('10.8'):
        exit("This tool only tested on 10.8+")

def kill_services():
    """On 10.12, both the locationd and cfprefsd services like to not respect
    preference changes so we force them to reload."""
    proc = subprocess.Popen(['/usr/bin/killall', '-9', 'cfprefsd'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc = subprocess.Popen(['/usr/bin/killall', '-9', 'locationd'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

def service_handler(action):
    """Loads/unloads System's location services job on supported OSs."""
    supported, current = LooseVersion('10.12.4'), LooseVersion(os_vers())
    if current < supported:
        print("LaunchD for locationd supported")
        if action is 'load':
            kill_services()
        launchctl = ['/bin/launchctl', action,
                     '/System/Library/LaunchDaemons/com.apple.locationd.plist']
        subprocess.check_output(launchctl)

def sysprefs_boxchk():
    """Disable location services in sysprefs globally."""
    uuid = get_hardware_uuid()
    perfdir = "/private/var/db/locationd/Library/Preferences/ByHost/"
    if not os.path.exists(perfdir):
        os.makedirs(perfdir)
    path_stub = "/private/var/db/locationd/Library/Preferences/ByHost/com.apple.locationd."
    das_plist = path_stub + uuid.strip() + ".plist"
    try:
        on_disk = FoundationPlist.readPlist(das_plist)
    except:
        plist = {}
        FoundationPlist.writePlist(plist, das_plist)
        on_disk = FoundationPlist.readPlist(das_plist)
    val = on_disk.get('LocationServicesEnabled', None)
    if val != 0:
        service_handler('unload')
        on_disk['LocationServicesEnabled'] = 0
        FoundationPlist.writePlist(on_disk, das_plist)
        os.chown(das_plist, 205, 205)
        service_handler('load')

def clear_clients():
    """Clear clients.plist in locationd settings."""
    auth_plist = {}
    das_plist = '/private/var/db/locationd/clients.plist'
    clients_dict = FoundationPlist.readPlist(das_plist)
    service_handler('unload')
    clients_dict = auth_plist
    FoundationPlist.writePlist(clients_dict, das_plist)
    os.chown(das_plist, 205, 205)
    service_handler('load')

def main():
    """Give main"""
    os_check()
    root_check()
    sysprefs_boxchk()
    clear_clients()

if __name__ == '__main__':
    main()
