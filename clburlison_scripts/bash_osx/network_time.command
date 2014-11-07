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



# Set Network time settings

#Primary Time server for Company Macs
                                                                  
TimeServer1=dccentral1.bisd.k12

#Secondary Time server for Company Macs

TimeServer2=dccentral2.bisd.k12

#Tertiary Time Server for Company Macs, used outside of Company network

TimeServer3=time.apple.com

# Time zone for Company Macs

TimeZone=America/Chicago

# Configure network time server and region

# Set the time zone
/usr/sbin/systemsetup -settimezone $TimeZone

# Set the primary network server with systemsetup -setnetworktimeserver
# Using this command will clear /etc/ntp.conf of existing entries and
# add the primary time server as the first line.

/usr/sbin/systemsetup -setnetworktimeserver $TimeServer1

# Add the secondary time server as the second line in /etc/ntp.conf
echo "server $TimeServer2" >> /etc/ntp.conf

# Add the tertiary time server as the third line in /etc/ntp.conf
#echo "server $TimeServer3" >> /etc/ntp.conf

# Enables the Mac to set its clock using the network time server(s)
/usr/sbin/systemsetup -setusingnetworktime on