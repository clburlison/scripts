#!/bin/bash

# https://groups.google.com/d/msg/macenterprise/5spqde8b9A4/JyvL5iPaGS4J

keep1="/Users/techsupport"
keep2="/Users/admin"
keep3="/Users/Shared"
keep4="/Users/teacher"
keep5="/Users/Guest1"

# Delete if the account is older than 30 days
USERLIST=`find /Users -type d -maxdepth 1 -mindepth 1 -not -name "." -mtime +30`

for a in $USERLIST ; do
    [[ "$a" == "$keep1" ]] && continue                    #skip account 1
    [[ "$a" == "$keep2" ]] && continue                    #skip account 2
    [[ "$a" == "$keep3" ]] && continue                    #skip account 3
    [[ "$a" == "$keep4" ]] && continue                    #skip account 4
    [[ "$a" == "$keep5" ]] && continue                    #skip account 5
    dscl . delete $a                                      #delete the account
done

# If you want to delete the home directories as well. Add the excluded users to the line below.
# find /Users -type d -maxdepth 1 -mindepth 1 -not \( -name "*admin*" -o -name "*Shared*" \) -mtime +30 -exec rm -rf {} \;
