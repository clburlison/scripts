#!/bin/bash

###################################################################################
#
# ADacctChange.sh
# This script will:
#  1) Wait for a specific point in the future before running
#  2) Check if bound to an AD Server
#  3) Check for an active network connection
#  4) Check for access to an AD Server
#  5) Search all local & Cached User Accounts on the current computer
#  6) Check with the AD Server and if the "User logon name" is different from
#     the Cached account with make the necessary changes on the Mac to update the account.
# 
# When running this script you will see an error message on L171. This is
# an intentional code design error. The script decides what accounts to modify
# based off of the $uniqueIDAD variable so if it errors on run I want to see the output. 
# If it does not error then that user account will be skipped.
#
# Hopefully all the check steps will verify data integrity before 
# doing something harmful...but as always test in your environment.
# I hold no responsibility for broken systems.
# 
#
# Maintainer: Clayton Burlison <https://clburlison.com>
# Last Modified: March 26th, 2015
#
#
# Special Thanks:
# 
# Rich Trouton <https://derflounder.wordpress.com/>
# Charles Edge <http://krypted.com/>
# Jeff Kelley <http://blog.slaunchaman.com/>
#
#
# References:
# https://groups.google.com/d/msg/macenterprise/p9hrMuvfECM/9Lz_aW63vyMJ
# https://github.com/rtrouton/rtrouton_scripts/blob/master/rtrouton_scripts/migrate_local_user_to_AD_domain/MigrateLocalUserToADDomainAcct.command
# http://blog.slaunchaman.com/2010/07/01/how-to-run-a-launchdaemon-that-requires-networking/
#
###################################################################################


###################################################################################
# 
# ~~~~~~~~~~~~~~~~~~~~~Variables~~~~~~~~~~~~~~~~~~
# 
# Time Variables
# Need the current date and time information in numeric values. This allows us to
# run the script at a specific point in the future.
# Format = YearMonthDayHourMinute ie: 1503242228 March 24, 2015 at 10:28pm
# 
###################################################################################

DCSERVER="bisd.k12"
DOMAIN="BISD"
# User accounts you do not want to modify.
keep1="/Users/techsupport"
keep2="/Users/Shared"
keep3="/Users/teacher"
setTime=1504060600

###################################################################################
# 
# ~~~~~~~~~~~~~~~~~~~~~End of Variables~~~~~~~~~~~~~~~~~~
# 
###################################################################################


###################################################################################
# 
# This script will only work as root.
# 
###################################################################################

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

###################################################################################
# 
# Check for Date/Time to see if it is time to run the script
# 
###################################################################################

curTime=`date +%y%m%d%H%M`
if [ "$setTime" -gt "$curTime" ]
    then
        echo "It is not time to run this script. Now exiting."
        exit 0
elif [ "$setTime" -lt "$curTime" ]
    then
        echo "It is time to change the Active Directory Cached User Accounts on this system."
else 
        echo "Date/Time value is invalid. Now exiting."
        exit 0
fi

###################################################################################
# 
# Test to make sure computer is bound to AD and has a active conneciton to an
# AD server
# 
###################################################################################

# If the machine is not bound to AD, then there's no purpose going any further.
check4AD=`/usr/bin/dscl localhost -list . | grep "Active Directory"`
if [ "${check4AD}" != "Active Directory" ]; then
	echo "This machine is not bound to Active Directory.\nPlease bind to AD first. ";
    /bin/rm /Library/LaunchDaemons/com.github.clburlison.ADacctChange.plist
    /bin/rm $0
fi

# Determine if the network is up by looking for any non-loopback internet network interfaces.
CheckForNetwork()
{
	local test
	if [ -z "${NETWORKUP:=}" ]; then
		test=$(ifconfig -a inet 2>/dev/null | sed -n -e '/127.0.0.1/d' -e '/0.0.0.0/d' -e '/inet/p' | wc -l)
		if [ "${test}" -gt 0 ]; then
			NETWORKUP="-YES-"
		else
			NETWORKUP="-NO-"
		fi
	fi
}

# If the network never becomes active this could run indefinitely
while [ "${NETWORKUP}" != "-YES-" ]
do
        sleep 5
        NETWORKUP=
        CheckForNetwork
done

# abort if we're not able to contact a configured directory server
ping -c 1 -t 1 $DCSERVER  > /dev/null 2>&1
if [ $? -eq 0 ]; then
 		ONLOCALNETWORK=YES
	echo "Computer is on the network: $ONLOCALNETWORK"
else
 		ONLOCALNETWORK=NO
	echo "Computer is on the network: $ONLOCALNETWORK"
	echo "Exiting. We cannot talk to the domain controller."
	exit 1
fi

###################################################################################
# 
# Check for Cached Active Directory User Accounts on Client Mac and make changes
# to the account if they do not match the new AD account.
# 
###################################################################################

USERLIST=`find /Users -type d -maxdepth 1 -mindepth 1 -not -name "."`
for a in $USERLIST ; do
    [[ "$a" == "$keep1" ]] && continue                    #skip account 1
    [[ "$a" == "$keep2" ]] && continue                    #skip account 2
    [[ "$a" == "$keep3" ]] && continue                    #skip account 3

    # need the following varriable to be silent
    uniqueIDAD=`/usr/bin/dscl /Active\ Directory/$DOMAIN/All\ Domains -read $a UniqueID | awk '{ print $2 }'`
    if [ "$uniqueIDAD" == "source" ]; then
        # we have bad data from dscl
        echo "We have received bad data from dscl. Now exiting."
        exit 0
    elif [ -z "$uniqueIDAD" ]; then    
        # The varraible is null. We need to modify the current Cached User:
        # the following will be changed "Account Name" and "Home Directory"?(maybe).
        prefix="/Users/"
        old=${a#$prefix}
        echo "Old username is: " $old
        CachedUID=`/usr/bin/id -u $old`
        echo "Cached UID is: " $CachedUID

        # Get new username as a variable from the Domain
        new=`/usr/bin/dscl /Active\ Directory/$DOMAIN/All\ Domains -search /Users UniqueID $CachedUID | awk 'NR==1{print $1; exit}'`
        echo "New username is: " $new
        
        # Move the old AD account to the new Account name. Essentially creating a new user account.
        /bin/mv /var/db/dslocal/nodes/Default/users/$old.plist /var/db/dslocal/nodes/Default/users/$new.plist
        /usr/bin/killall opendirectoryd
        sleep 10

        # edit new user attributes on new user, using same passwd hash
        /usr/bin/dscl . -change /Users/$old RecordName $old $new
        sleep 3
        /usr/bin/dscl . -change /Users/$new NFSHomeDirectory /Users/$old /Users/$new
        sleep 3

        /usr/bin/killall opendirectoryd
        # Move Home Directory. Check if there's a home folder there already, if there is, exit before we wipe it
        if [ -f /Users/$new ]; then
            echo "Oops, theres a home folder there already for $new.\nIf you don't want that one, delete it in the Finder first,\nthen run this script again."
        else
            /bin/mv /Users/$old /Users/$new
            /usr/sbin/chown -R ${new} /Users/$new
            #/usr/bin/dscl . -append /Users/$new RecordName $old
            echo "Home for $new now located at /Users/$new"
        fi
    fi
done


###################################################################################
# 
# Remove this script and launchDaemon. Lastly reboot the system.(?)
# 
###################################################################################

/bin/rm /Library/LaunchDaemons/com.github.clburlison.ADacctChange.plist
/bin/rm $0

/sbin/reboot