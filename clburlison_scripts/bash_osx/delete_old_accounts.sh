#!/bin/bash

# https://github.com/rsaeks/scripts/

keep1="/Users/studentuser"
keep2="/Users/admin"
keep3="/Users/Shared"
keep4="/Users/teacher"
keep5="/Users/Guest1"

USERLIST=`find /Users -type d -maxdepth 1 -mindepth 1 -not -name "." -mtime +30`

for a in $USERLIST ; do
    [[ "$a" == "$keep1" ]] && continue                    #skip account 1
    [[ "$a" == "$keep2" ]] && continue                    #skip account 2
    [[ "$a" == "$keep3" ]] && continue                    #skip account 3
    [[ "$a" == "$keep4" ]] && continue                    #skip account 4
    [[ "$a" == "$keep5" ]] && continue                    #skip account 5
	dscl . delete $a                                      #delete the account
done