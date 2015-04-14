#!/bin/bash

account=`dsconfigad -show | awk '/Computer *Account/ { print $4 }'` \
&& printf "AD Computer Account: ${account}\nAD Computer Password: \
`sudo security find-generic-password -a ${account} -w /Library/Keychains/System.keychain`\n"
read dummy