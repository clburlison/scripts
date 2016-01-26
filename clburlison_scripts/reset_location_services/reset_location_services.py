#!/usr/bin/python
"""Reset location services to factory settings. Requires FoundationPlist
which is installed by default with munki - https://github.com/munki/munki/releases"""

import sys, os, platform, subprocess, objc
from Foundation import NSRunLoop, NSDate, NSObject
from Foundation import NSBundle
try:
    sys.path.append('/usr/local/munki/munkilib/')
    import FoundationPlist
except ImportError as error:
    print "Could not find FoundationPlist, are munkitools installed?"
    raise error

# Retrieve system UUID
IOKit_bundle = NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')

functions = [("IOServiceGetMatchingService", b"II@"),
             ("IOServiceMatching", b"@*"),
             ("IORegistryEntryCreateCFProperty", b"@I@@I"),
            ]

objc.loadBundleFunctions(IOKit_bundle, globals(), functions)
    
def io_key(keyname):
    return IORegistryEntryCreateCFProperty(IOServiceGetMatchingService(0, IOServiceMatching("IOPlatformExpertDevice")), keyname, None, 0)

def get_hardware_uuid():
    return io_key("IOPlatformUUID")

def root_check():
    """Check for root access."""
    if not os.geteuid() == 0:
        exit("This must be run with root access.")

def os_vers():
    """Retrieve OS version."""
    maj_os_vers = platform.mac_ver()[0].split('.')[1]
    return maj_os_vers

def os_check():
    """Only tested on 10.8 - 10.11."""
    if not (8 <= int(os_vers()) <= 11):
        exit("This tool only tested on 10.8 - 10.11")

def service_handler(action):
    """Loads/unloads System's location services launchd job."""
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
        p = {}
        FoundationPlist.writePlist(p, das_plist)
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
    root_check()
    sysprefs_boxchk()
    clear_clients()

if __name__ == '__main__':
    main()