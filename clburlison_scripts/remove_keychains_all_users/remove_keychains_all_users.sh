#!/bin/sh

# Remove all keychains on the local system.
# Useful in lab settings.
# Use with extreme caution.

# Run as root

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


# Remove keychains

for USER_HOME in /Users/*
  do
    USER_UID=`basename "${USER_HOME}"`
    if [ ! "${USER_UID}" = "Shared" ] 
     then 
      if [ -d "${USER_HOME}"/Library/Keychains ]
       then
        rm -rf "${USER_HOME}"/Library/Keychains/*
      fi
    fi
  done

# In some situations it might make sense to reboot
# /sbin/reboot