#!/bin/bash
#
# Author: Clayton Burlison <https://clburlison.com>
# Date: Oct. 19, 2015
#
# Useful for fixing the permissions of AD accounts. When you manually 
#  copy the contents of /Users/some_username_here to another Mac
#  you need to modify the permissions of that account so the user 
#  can login. This is useful when you Backup/Restore to another Mac.

USERLIST=`find /Users -type d -maxdepth 1 -mindepth 1 -not -name "."`

for a in $USERLIST ; do
  [[ "$a" == "/Users/Shared" ]] && continue # Do not modify the Shared Folder
  [[ "$a" == "/Users/root" ]] && continue # Do not modify the root Folder
  
  # Get User UUID
  acct=${a#"/Users/"}
  ID=`id -u $acct`

  # Fix permissions to match the UUID.
  /usr/sbin/chown -R ${ID} ${a}  
done

exit 0