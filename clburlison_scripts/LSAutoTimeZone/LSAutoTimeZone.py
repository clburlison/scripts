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
import objc
from CoreLocation import CLLocationManager
from Foundation import NSBundle
from Foundation import NSData
from Foundation import NSPropertyListSerialization
from Foundation import NSPropertyListMutableContainers
from Foundation import NSPropertyListXMLFormat_v1_0

NTP_SERVERS = ['time1.google.com', 'time.apple.com']


# class FoundationPlistException(Exception):
#     """Basic exception for plist errors"""
#     pass
#
#
# class NSPropertyListSerializationException(FoundationPlistException):
#     """Read/parse error for plists"""
#     pass
#
#
# class NSPropertyListWriteException(FoundationPlistException):
#     """Write error for plists"""
#     pass
#
#
# def readPlist(filepath):
#     """
#     Stolen from Munki FoundationPlist.py
#     Read a .plist file from filepath.  Return the unpacked root object
#     (which is usually a dictionary).
#     """
#     plistData = NSData.dataWithContentsOfFile_(filepath)
#     dataObject, dummy_plistFormat, error = (
#         NSPropertyListSerialization.
#         propertyListFromData_mutabilityOption_format_errorDescription_(
#             plistData, NSPropertyListMutableContainers, None, None))
#     if dataObject is None:
#         if error:
#             error = error.encode('ascii', 'ignore')
#         else:
#             error = "Unknown error"
#         errmsg = "%s in file %s" % (error, filepath)
#         raise NSPropertyListSerializationException(errmsg)
#     else:
#         return dataObject
#
#
# def writePlist(dataObject, filepath):
#     """
#     Stolen from Munki FoundationPlist.py
#     Write 'rootObject' as a plist to filepath.
#     """
#     plistData, error = (
#         NSPropertyListSerialization.
#         dataFromPropertyList_format_errorDescription_(
#             dataObject, NSPropertyListXMLFormat_v1_0, None))
#     if plistData is None:
#         if error:
#             error = error.encode('ascii', 'ignore')
#         else:
#             error = "Unknown error"
#         raise NSPropertyListSerializationException(error)
#     else:
#         if plistData.writeToFile_atomically_(filepath, True):
#             return
#         else:
#             raise NSPropertyListWriteException(
#                 "Failed to write plist data to %s" % filepath)


def get_hardware_uuid():
    """Get the UUID of the computer"""
    # IOKit Bundle Objective C code from Michael Lynn
    # https://gist.github.com/pudquick/c7dd1262bd81a32663f0
    uuid = ''
    IOKit_bundle = NSBundle.bundleWithIdentifier_(
        'com.apple.framework.IOKit')
    functions = [("IOServiceGetMatchingService", b"II@"),
                 ("IOServiceMatching", b"@*"),
                 ("IORegistryEntryCreateCFProperty", b"@I@@I"), ]
    IOKit = dict()
    objc.loadBundleFunctions(IOKit_bundle, IOKit, functions)
    # pylint:disable=F0401, E0602, W0232
    uuid = IOKit['IORegistryEntryCreateCFProperty'](
        IOKit['IOServiceGetMatchingService'](
            0, IOKit['IOServiceMatching'](
                'IOPlatformExpertDevice')), 'IOPlatformUUID', None, 0)
    return uuid


def root_check():
    """Check for sudo access"""
    if not os.geteuid() == 0:
        exit("This must be run with sudo")


def os_vers():
    """Retrieve OS version."""
    maj_os_vers = platform.mac_ver()[0].split('.')[1]
    return maj_os_vers


def os_check():
    """Should be good on 10.8 and above"""
    maj_os_vers = platform.mac_ver()[0].split('.')[1]
    if not 8 <= int(maj_os_vers):
        exit("Your OS is not supported at this time: %s" %
             platform.mac_ver()[0])


def sysprefs_boxchk():
    """Enables location services in sysprefs globally."""
    uuid = get_hardware_uuid()
    prefdir = "/private/var/db/locationd/Library/Preferences/ByHost/"
    if not os.path.exists(prefdir):
        os.makedirs(prefdir)
    das_plist = ("/private/var/db/locationd/Library/Preferences"
                 "/ByHost/com.apple.locationd.{0}.plist".format(uuid.strip()))
    bkup_plist = ("/private/var/db/locationd/Library/Preferences"
                  "/ByHost/com.apple.locationd.notbackedup.{0}.plist".format(
                   uuid.strip()))

    # Use the offical Apple API for determining location services status
    ls_status = CLLocationManager.locationServicesEnabled()
    if ls_status is not True:
        service_handler('unload')
        cmd = ['/usr/bin/defaults', 'write', das_plist,
               'LocationServicesEnabled', '-int', '1']
        subprocess.check_output(cmd)
        os.chown(das_plist, 205, 205)

        # 10.12 created a new 'notbackedup' file and although changing it
        # is not necessary, we are making the change so it matches Apple's
        # implementation.
        if int(os_vers()) >= 12:
            cmd = ['/usr/bin/defaults', 'write', bkup_plist,
                   'LocationServicesEnabled', '-int', '1']
            subprocess.check_output(cmd)
            os.chown(bkup_plist, 205, 205)
        service_handler('load')


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
    """Loads or unloads System's location services launchd job"""
    if action is 'load':
        kill_services()
    launchctl = ['/bin/launchctl', action,
                 '/System/Library/LaunchDaemons/com.apple.locationd.plist']
    subprocess.check_output(launchctl)


def autoset_timezone():
    """Enable Set time zone automatically using current location"""
    auto_plist = '/Library/Preferences/com.apple.timezone.auto.plist'
    cmd = ['/usr/bin/defaults', 'write', auto_plist, 'Active', '-int', '1']
    subprocess.check_output(cmd)


def timezone_lookup():
    """Force a timezone lookup right now"""
    TZPP = NSBundle.bundleWithPath_("/System/Library/PreferencePanes/"
                                    "DateAndTime.prefPane/Contents/"
                                    "Resources/TimeZone.prefPane")
    TimeZonePref = TZPP.classNamed_('TimeZonePref')
    ATZAdminPrefererences = TZPP.classNamed_('ATZAdminPrefererences')
    atzap = ATZAdminPrefererences.defaultPreferences()
    pref = TimeZonePref.alloc().init()
    atzap.addObserver_forKeyPath_options_context_(pref, "enabled", 0, 0)
    result = pref._startAutoTimeZoneDaemon_(0x1)
    # If this is not set to 1 then AutoTimezone still isn't enabled.
    # This additional preference check makes this script work with 10.12
    if pref.isTimeZoneAutomatic() is not 1:
        return False
    return True



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
    if timezone_lookup() is not True:
        print ("Automatic Time Zone was not enabled or your machine"
               "doesn't support properly this functionality")
        sys.exit(1)
    # enable_ntp()

if __name__ == '__main__':
    main()
