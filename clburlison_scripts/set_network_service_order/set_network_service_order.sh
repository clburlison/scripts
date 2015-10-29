#!/bin/bash
# @erikberglund, @elvisizer - macadmins.slack.com #bash channel
while read networkService; do
	if [[ ${networkService} =~ .*Ethernet.* ]] || [[ ${networkService} =~ .*Thunderbolt.* ]]; then
		prioritizedServices+=( "${networkService}" )
	elif [[ ${networkService} =~ .*Bluetooth.* ]] || [[ ${networkService} =~ .*FireWire.* ]]; then
		deprioritizedServices+=( "${networkService}" )
	else
		otherServices+=( "${networkService}" )
	fi
done < <( networksetup -listnetworkserviceorder | awk '/^\([0-9]/{$1 ="";gsub("^ ","");print}' )
networksetup -ordernetworkservices "${prioritizedServices[@]}" "${otherServices[@]}" "${deprioritizedServices[@]}"
exit 0