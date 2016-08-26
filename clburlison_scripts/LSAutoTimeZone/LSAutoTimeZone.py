#!/usr/bin/python
"""
This script has a bunch of stolen work from @arubdesu, @pudquick, and Munki. 
It is completely self contained and should do the following:

1. Enable Location Services globally
2. Enable "Set time zone automatically using current location"
3. Force a time zone location lookup at runtime
4. Set correct date, time, and time zone

Optionally set NTP servers.

References/borrowed code:
https://gist.github.com/arubdesu/b72585771a9f606ad800
https://gist.github.com/pudquick/ba235b7e90aafb9986158697a457a0d0
https://github.com/rtrouton/rtrouton_scripts/blob/master/rtrouton_scripts/time_settings/time_settings.sh
https://github.com/munki/munki/blob/master/code/client/munkilib/FoundationPlist.py
"""

import os
import platform
import subprocess
import sys
from Foundation import NSBundle
from Foundation import NSData
from Foundation import NSPropertyListSerialization
from Foundation import NSPropertyListMutableContainers
from Foundation import NSPropertyListXMLFormat_v1_0

NTP_SERVERS = ['time1.google.com', 'time.apple.com']

class FoundationPlistException(Exception):
    """Basic exception for plist errors"""
    pass


class NSPropertyListSerializationException(FoundationPlistException):
    """Read/parse error for plists"""
    pass


class NSPropertyListWriteException(FoundationPlistException):
    """Write error for plists"""
    pass


def readPlist(filepath):
    """
    Stolen from Munki FoundationPlist.py
    Read a .plist file from filepath.  Return the unpacked root object
    (which is usually a dictionary).
    """
    plistData = NSData.dataWithContentsOfFile_(filepath)
    dataObject, dummy_plistFormat, error = (
        NSPropertyListSerialization.
        propertyListFromData_mutabilityOption_format_errorDescription_(
            plistData, NSPropertyListMutableContainers, None, None))
    if dataObject is None:
        if error:
            error = error.encode('ascii', 'ignore')
        else:
            error = "Unknown error"
        errmsg = "%s in file %s" % (error, filepath)
        raise NSPropertyListSerializationException(errmsg)
    else:
        return dataObject


def writePlist(dataObject, filepath):
    """
    Stolen from Munki FoundationPlist.py
    Write 'rootObject' as a plist to filepath.
    """
    plistData, error = (
        NSPropertyListSerialization.
        dataFromPropertyList_format_errorDescription_(
            dataObject, NSPropertyListXMLFormat_v1_0, None))
    if plistData is None:
        if error:
            error = error.encode('ascii', 'ignore')
        else:
            error = "Unknown error"
        raise NSPropertyListSerializationException(error)
    else:
        if plistData.writeToFile_atomically_(filepath, True):
            return
        else:
            raise NSPropertyListWriteException(
                "Failed to write plist data to %s" % filepath)


def ioreg():
    """get UUID to find locationd plist with"""
    cmd = ['/usr/sbin/ioreg', '-rd1', '-c', 'IOPlatformExpertDevice']
    full_reg = subprocess.check_output(cmd)
    reg_list = full_reg.split('\n')
    for reg in reg_list:
        if reg.startswith('      "IOPlatformUUID"'):
            uuid = reg[26:-1]
    return uuid


def root_check():
    """Check for sudo access"""
    if not os.geteuid() == 0:
        exit("This must be run with sudo")


def os_check():
    """Should be good on 10.8 and above"""
    maj_os_vers = platform.mac_ver()[0].split('.')[1]
    if not 8 <= int(maj_os_vers):
        exit("Your OS is not supported at this time: %s" % platform.mac_ver()[0])


def sysprefs_boxchk():
    """Enables location services in sysprefs globally"""
    uuid = ioreg()
    path_stub = "/private/var/db/locationd/Library/Preferences/ByHost/com.apple.locationd."
    das_plist = path_stub + uuid.strip() + ".plist"
    on_disk = readPlist(das_plist)
    val = on_disk.get('LocationServicesEnabled', None)
    if val != 1:
        on_disk['LocationServicesEnabled'] = 1
        writePlist(on_disk, das_plist)
        os.chown(das_plist, 205, 205)


def service_handler(action):
    """Loads or unloads System's location services launchd job"""
    launchctl = ['/bin/launchctl', action,
                 '/System/Library/LaunchDaemons/com.apple.locationd.plist']
    subprocess.check_output(launchctl)


def autoset_timezone():
    """Enable Set time zone automatically using current location"""
    das_plist = '/Library/Preferences/com.apple.timezone.auto.plist'
    enabler = dict()
    try:
        enabler = readPlist(das_plist)
        val = enabler.get('Active')
    except:
        val = 0
    if val != 1:
        enabler['Active'] = 1
    writePlist(enabler, das_plist)


def timezone_lookup():
    """Force a timezone lookup right now"""
    TZPP = NSBundle.bundleWithPath_("/System/Library/PreferencePanes/DateAndTime.prefPane/Contents/Resources/TimeZone.prefPane")
    TimeZonePref = TZPP.classNamed_('TimeZonePref')
    pref = TimeZonePref.alloc().init()
    result = pref._startAutoTimeZoneDaemon_(0x1)


def enable_ntp():
    """Enable your Mac to use NTP to set clock time and set NTP servers"""
    ntpconf = open('/etc/ntp.conf', 'w')
    for server in NTP_SERVERS:
      ntpconf.write("{0}{1}\n".format('server ', server))
    enable_ntp = ['/usr/sbin/systemsetup', '-setusingnetworktime', 'on']
    subprocess.check_output(enable_ntp)


def main():
    """gimme some main"""
    root_check()
    os_check()
    service_handler('unload')
    sysprefs_boxchk()
    service_handler('load')
    autoset_timezone()
    timezone_lookup()
    # enable_ntp()

if __name__ == '__main__':
    main()
