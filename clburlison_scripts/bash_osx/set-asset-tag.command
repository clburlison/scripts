#!/bin/bash

RunAsRoot()
{
        ## Pass in the full path to the executable as $1
        if [[ "${USER}" != "root" ]] ; then
echo
echo "*** This application must be run as root. Please authenticate below. ***"
                echo
sudo "${1}" && exit 0
        fi
}

RunAsRoot "${0}"

read -p "Enter asset tag number : " asset

echo Setting asset tag number.

defaults write /Library/Preferences/com.apple.RemoteDesktop.plist Text2 $asset
