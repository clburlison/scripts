#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/libexec:/usr/local/bin export PATH


# Must be the root user to run this application
##################################################################################################################
# RunAsRoot()
# {
#         ## Pass in the full path to the executable as $1
#         if [[ "${USER}" != "root" ]] ; then
# echo
# echo "*** This application must be run as root. Please authenticate below. ***"
#                 echo
# sudo "${1}" && exit 0
#         fi
# }
#
# RunAsRoot "${0}"
##################################################################################################################


#debug mode variables, comment out the following block of code if you wish to not have a debug log
##################################################################################################################
# DATE=`date +%Y-%m-%d_%H:%M:%S`
# APP_NAME="LocalAdminMembershipUpdater"
# LOG_LOCATION="/Library/Logs/$APP_NAME"
# mkdir -p "$LOG_LOCATION"
# LOG_FILE_NAME="$APP_NAME"_"$DATE".log
# find "$LOG_LOCATION" -mtime +14 -exec rm '{}' \; #delete logs 14 days old
# set -x
# exec 1>>"$LOG_LOCATION"/"$LOG_FILE_NAME" 2>&1
##################################################################################################################


# Custom Settings
##################################################################################################################
# Additional Array of quoted groups to check separated by spaces:
# i.e. CUSTOMGROUPS=("Teachers" "Students" "Faculty" "MYDOMAIN\enterprise admins")
CUSTOMGROUPS=()
DCSERVER="domain_server"
##################################################################################################################


# Main Program Below
##################################################################################################################

# enumerate through all users.
dscl . list /Users | grep -v "^_" | while read USERNAME; do
	
	# ignore local users, they shouldn't need to be modified
	LOCALCHECK=`dscl /Local/Default -read /Users/"$USERNAME" AuthenticationAuthority | grep "LocalCachedUser"`
	if [ "$LOCALCHECK" == "" ]; then
		echo "Ignoring user $USERNAME because they are a local user."
		continue
	else
		echo "The user $USERNAME is cached local user. Continuing."
	fi
	
	# abort if we're not able to contact a configured directory server
 	ping -c 1 -t 1 $DCSERVER  > /dev/null 2>&1
 	if [ $? -eq 0 ]; then
 		ONLOCALNETWORK=YES
		echo "Computer is on the network: $ONLOCALNETWORK"
 	else
 		ONLOCALNETWORK=NO
		echo "Computer is not on the network: $ONLOCALNETWORK"
		echo "Exiting. We can not talk to the domain controller."
		exit 1
	fi
	

	# Set the default admin value which should be off
	USERISADMIN=NO


	IFS=$','
	# Check the array of admin groups defined in the AD plugin
	ADMIN_RESULTS=`dsconfigad -show | grep "Allowed admin" | awk 'BEGIN { FS="= " } ; { print $2 }'`
	
	for ADMINGROUP in $ADMIN_RESULTS; do
		if (dseditgroup -o checkmember -m "$USERNAME" "$ADMINGROUP" > /dev/null); then
			USERISADMIN=YES
			echo "User $USERNAME found to be a member of the group $ADMINGROUP from the AD plugin admin groups."
		fi
	done
	
  	IFS=$oIFS
	
	# enumerate through the custom list of groups
	GROUPCOUNT=${#CUSTOMGROUPS[@]}
	if [ $GROUPCOUNT -ne 0 ]; then
		for i in ${CUSTOMGROUPS[@]}; do
			if (dseditgroup -o checkmember -m "$USERNAME" "$i" > /dev/null); then
				USERISADMIN=YES
				echo "User $USERNAME found to be a member of the group $i from the custom admin group array customizable in this script."
			fi
		done
	fi
	
	# modify the admin group if needed	
	echo "Is the user $USERNAME an admin based on group membership lookup? $USERISADMIN!"
	if [ "$USERISADMIN" == "YES" ]; then
		echo "Adding user $USERNAME to the local admin group!"
		dseditgroup -o edit -a "$USERNAME" -t user -n /Local/Default admin	
	else
		echo "Removing user $USERNAME from the local admin group!"
		dseditgroup -o edit -d "$USERNAME" -t user -n /Local/Default admin	
	fi
done

exit 0;
##################################################################################################################
