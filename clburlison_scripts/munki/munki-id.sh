#!/bin/sh
SYSCLIENTID=$(scutil --get ComputerName)
sudo defaults write /Library/Preferences/ManagedInstalls ClientIdentifier $SYSCLIENTID
touch "/Users/Shared/.com.googlecode.munki.checkandinstallatstartup"
sudo reboot
exit 0