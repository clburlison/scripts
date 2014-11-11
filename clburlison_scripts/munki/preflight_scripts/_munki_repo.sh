#!/bin/sh

# This preflight is useful if you have an internal site and an external site or if you have two servers serving your munki clients.
# This script will apply a simple fail over from server1 to server2. 

ping -c 1 -t 1 server1 > /dev/null 2>&1
if [ $? -eq 0 ]; then
	echo "Connected to server1"
	sudo defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL "http://server1.example.com/munki_repo"
else
	echo "Connected to server2"
	sudo defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL "http://server2.example.com/munki_repo"
fi
exit