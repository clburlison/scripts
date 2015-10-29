#!/bin/bash
# This will retrieve the primary interface of a Mac and 
# exit the munki check flight script if on wireless.
PORT=$(route get 0.0.0.0 2>/dev/null | awk '/interface: / {print $2}')
IS_WIRELESS=$(networksetup -getairportnetwork $PORT | awk 'NR==1')

if [[ "$IS_WIRELESS" == *"is not a Wi-Fi interface"* ]]
  then
      echo "Default route is a Wired interface."
  else
      # We're on a wireless connection, exit this package install
      echo "Default route is a Wi-Fi interface."
      exit 1
fi