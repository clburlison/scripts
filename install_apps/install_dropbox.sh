#!/bin/bash
echo 'Enter your local admin password below (needed install Dropbox to /Applications):'
cd /tmp; curl -O https://d1ilhw0800yew8.cloudfront.net/client/Dropbox%202.8.3.dmg;
hdiutil attach -nobrowse ./Dropbox%202.8.3.dmg
sudo cp -R "/Volumes/Dropbox Installer/Dropbox.app" /Applications/
# hdiutil detach "/Volumes/Dropbox Installer"
rm Dropbox%202.8.3.dmg
open /Applications/Dropbox.app
echo 'After Dropbox has started syncing the files needed click enter to continue.'
read dummy
