#!/bin/bash

# Origin: https://groups.google.com/d/msg/macenterprise/HgWHx3L5KtE/lLu6dbEDQxEJ by Tim Perfitt
# Modified by: Clayton Burlison on May 22nd, 2014 to work for Birdville ISD

currentuser=$USER
smbhome="$(dscl '/Active Directory/BISD/All Domains/' -read /Users/$currentuser SMBHome)"

if [ $? != "0" ] ; then
        echo could not get smb home.  Offline?
        exit

fi

smbhome=$(echo $smbhome|awk '{print "smb:"$2}'|tr "\\" "//")

if [ "$smbhome" == 'smb:' ] ; then 
        echo could not get smb home.  Not defined for user $currentuser?
        exit
fi

mkdir -p /Volumes/$currentuser
mount -t smbfs $smbhome /Volumes/$currentuser