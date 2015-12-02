#!/bin/bash
#
# Author - Clayton Burlison
#
# Updates:
#   July 14, 2015    - Initial release 
#   October 14, 2015 - Use -currentHost flag instead of $UUID
#   December 2, 2015 - Updated for El Captain, now using a new preference
#

defaults -currentHost write com.apple.ImageCapture2 HotPlugActionPath ""
defaults -currentHost write com.apple.ImageCapture2 LastHotPlugActionPath ""
defaults -currentHost write com.apple.ImageCapture disableHotPlug -bool YES
exit 0