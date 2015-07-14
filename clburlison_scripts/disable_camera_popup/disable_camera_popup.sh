#!/bin/bash
#
# Author - Clayton Burlison (July 14, 2015)
#

UUID=`ioreg -rd1 -c IOPlatformExpertDevice | awk '/IOPlatformUUID/ { split($0, line, "\""); printf("%s\n", line[4]); }'`
defaults write ~/Library/Preferences/ByHost/com.apple.ImageCapture2.$UUID.plist HotPlugActionPath ""
defaults write ~/Library/Preferences/ByHost/com.apple.ImageCapture2.$UUID.plist LastHotPlugActionPath ""
