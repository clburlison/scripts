#!/bin/bash
echo 'This bootstrap script will guide you through setting up boxen:'
echo 'Click enter to cont.'
read dummy
xcode-select --install

echo 'Wait until command line tools finished installing before continuing.'
echo 'Click enter after it is complete'
echo ' '
read dummy

echo 'I have dependancies on files located on Dropbox.'
echo 'Lets manually install Dropbox so we can start the sync process.'
echo 'Enter your local admin password below (needed install Dropbox to /Applications):
cd /tmp; curl -O https://dl.dropboxusercontent.com/s/tb6hybu5qothudx/Dropbox%202.8.0.dmg;
hdiutil attach -nobrowse ./Dropbox%202.8.0.dmg
sudo cp -R "/Volumes/Dropbox Installer/Dropbox.app" /Applications/
# hdiutil detach "/Volumes/Dropbox Installer"
rm Dropbox%202.8.0.dmg
open /Applications/Dropbox.app
echo 'After Dropbox has started syncing the files needed click enter to continue.'
echo 'This will start the installation of boxen.'
read dummy


echo ' '
echo 'Enter your local admin password below:'
sudo mkdir -p /opt/boxen
sudo chown ${USER}:admin /opt/boxen
git clone https://github.com/clburlison/my-boxen.git /opt/boxen/repo
cd /opt/boxen/repo


# Do not require encryption (Useful for development):
./script/boxen --no-fde

# add boxen to your shell config, at the end, eg. This is done with my dotfiles repo
# echo '[ -f /opt/boxen/env.sh ] && source /opt/boxen/env.sh'>> ~/.bashrc

echo "You need to setup your shell profile to work with boxen. For me I need to setup my dotfiles."
echo " "
echo "Setup dotfiles with the following command:"
echo "cd src/mine/dotfiles; ./bootstrap.sh"
echo "boxen --env"
read dummy