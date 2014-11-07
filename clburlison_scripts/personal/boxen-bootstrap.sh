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
echo 'Go manually download. Don't worry I'll wait.'
echo 'Click enter to continue.'
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
echo "cd ~/src/mine/dotfiles; ./bootstrap.sh"
echo "boxen --env"
read dummy
