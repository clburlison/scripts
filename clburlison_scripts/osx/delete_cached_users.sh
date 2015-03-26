#!/bin/bash

# https://groups.google.com/d/msg/macenterprise/5spqde8b9A4/n1kz4WlCB7cJ

for user in `dscl localhost list /Local/Default/Users`
do
        isCached=`dscl localhost read /Local/Default/Users/$user | grep LDAP | wc -l | sed "s/[^0-9]*//g"`
        if [[ $isCached != 0 ]]
        then
                echo -n "Deleting cached account ${user}..."
                dscl localhost delete /Local/Default/Users/$user
                if [ -d "/Users/${user}" ]
                then
                        rm -rf "/Users/${user}"
                fi
                echo "DONE"
        fi
done