#!/usr/bin/python
"""Reset location services to factory settings."""

import os
import platform
import subprocess

from distutils.version import LooseVersion


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
    read_cmd = ['/usr/bin/sudo', '-u', '_locationd', '/usr/bin/defaults',
                '-currentHost', 'read', 'com.apple.locationd',
                'LocationServicesEnabled']
    status = subprocess.check_output(read_cmd)
    if int(status) != 0:
        write_cmd = ['/usr/bin/sudo', '-u', '_locationd', '/usr/bin/defaults',
                     '-currentHost', 'write', 'com.apple.locationd',
                     'LocationServicesEnabled', '-bool', 'FALSE']
        subprocess.check_output(write_cmd)


def clear_clients():
    """Clear clients.plist in locationd settings."""
    cmd = ['/usr/bin/sudo', '-u', '_locationd', '/usr/bin/defaults',
           'delete', '/private/var/db/locationd/clients.plist']
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    kill_services()


def main():
    """Give main"""
    os_check()
    root_check()
    sysprefs_boxchk()
    clear_clients()


if __name__ == '__main__':
    main()
