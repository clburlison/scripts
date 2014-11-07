#!/bin/bash
LONDON1=$( ifconfig | grep '192.168.80' -c )
LONDON2=$( ifconfig | grep '192.168.121' -c )
TOKYO=$( ifconfig | grep '10.10.60' -c )
SHANGHAI=$( ifconfig | grep '10.10.185' -c )
SINGAPORE=$( ifconfig | grep '192.168.3' -c )
NEWYORK=$( ifconfig | grep '10.10.181' -c )
MUMBAI=$( ifconfig | grep '10.10.190' -c )


if [ $LONDON1 == 1 ]
then
echo "You are in London"
defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL "http://192.168.80.14/munki_repo"
defaults write /Library/Preferences/ManagedInstalls ClientIdentifier "munki_client"

fi

if [ $LONDON2 == 1 ]
then
echo "you are on London Aruba"
defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL "http://192.168.80.14/munki_repo"
defaults write /Library/Preferences/ManagedInstalls ClientIdentifier "munki_client"

fi

if [ $TOKYO == 1 ]
then
echo "you are in Tokyo"
defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL "http://192.168.80.14/munki_repo"
defaults write /Library/Preferences/ManagedInstalls ClientIdentifier "munki_client"
defaults write /Library/Preferences/ManagedInstalls PackageURL "http://10.10.60.90/munki_repo/pkgs"

fi

if [ $SHANGHAI == 1 ]
then
echo "you are in Shanghai, you don't have a server yet"

fi

if [ $SINGAPORE == 1 ]
then
echo "you are in Singapore"
defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL "http://192.168.80.14/munki_repo"
defaults write /Library/Preferences/ManagedInstalls ClientIdentifier "munki_client"
defaults write /Library/Preferences/ManagedInstalls PackageURL "http://192.168.3.135/munki_repo/pkgs”
fi

if [ $NEWYORK == 1 ]
then
echo "you are in New York, you don't have a server yet"
fi

if [ $MUMBAI == 1 ]
then
echo "you are in Mumbai"
defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL "http://192.168.80.14/munki_repo"
defaults write /Library/Preferences/ManagedInstalls ClientIdentifier "munki_client"
defaults write /Library/Preferences/ManagedInstalls PackageURL "http://10.10.190.14/munki_repo/pkgs”
fi

exit