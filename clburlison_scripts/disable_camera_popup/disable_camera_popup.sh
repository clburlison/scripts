#!/bin/bash
#
# Author - Clayton Burlison
#
# Updates:
#   July 14, 2015    - Initial release 
#   October 14, 2015 - Use -currentHost flag instead of $UUID 
#

defaults -currentHost write com.apple.ImageCapture2 HotPlugActionPath ""
defaults -currentHost write com.apple.ImageCapture2 LastHotPlugActionPath ""
exit 0