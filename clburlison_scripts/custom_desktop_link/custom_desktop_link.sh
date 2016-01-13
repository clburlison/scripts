#!/bin/bash
# Author: erikberglund
# Source: https://macadmins.slack.com/archives/bash/p1452707807001310

webloc_url="https://google.com"
webloc_name="Google" #Don't add .webloc to the name
webloc_folder_path="$HOME/Desktop"
webloc_icon="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ProfileBackgroundColor.icns"

## Create webloc path from script variables
webloc_path="${webloc_folder_path}/${webloc_name}.webloc"

## Create the webloc
/usr/libexec/PlistBuddy -c "Add :URL string ${webloc_url}" "${webloc_path}" > /dev/null 2>&1

## Set icns as icon for the webloc
python - "${webloc_icon}" "${webloc_path}"<< END
import Cocoa
import sys
Cocoa.NSWorkspace.sharedWorkspace().setIcon_forFile_options_(Cocoa.NSImage.alloc().initWithContentsOfFile_(sys.argv[1].decode('utf-8')), sys.argv[2].decode('utf-8'), 0) or sys.exit("Unable to set file icon")
END

## Hide .webloc file extension and tell file it's using a custom icon
## This line is removed as SetFile is only available if you install Command Line Tools
# /usr/bin/SetFile -a CE "${webloc_path}"

exit 0