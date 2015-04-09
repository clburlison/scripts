#!/bin/sh
sudo rm -r /var/root/Library/Preferences/com.apple.SoftwareUpdate.plist
sudo rm -r /Library/Preferences/com.apple.SoftwareUpdate.plist
sudo defaults delete /Library/Preferences/ManagedInstalls SoftwareUpdateServerURL