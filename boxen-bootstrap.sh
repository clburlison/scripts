#!/bin/bash
echo 'This bootstrap script will guide you through setting up boxen:'
echo 'Click enter to cont.'
read dummy
xcode-select --install

echo ' '
echo 'This is your local admin password:'
sudo mkdir -p /opt/boxen
sudo chown ${USER}:admin /opt/boxen
git clone https://github.com/clburlison/my-boxen.git /opt/boxen/repo
cd /opt/boxen/repo


# The beginning flag is because of an Apple bug with the new version of xcode. https://github.com/boxen/our-boxen/issues/528
# This should have been fixed in https://github.com/boxen/our-boxen/commit/d254b360c9cec4b2d82e83f18218672bf5886a18
#ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future ./script/boxen --no-fde

# Do not require encryption (Useful for development):
./script/boxen --no-fde

# add boxen to your shell config, at the end, eg. This is done with my dotfiles repo
# echo '[ -f /opt/boxen/env.sh ] && source /opt/boxen/env.sh'>> ~/.bashrc


echo "You need to setup your shell profile to work with boxen. For me I need to setup my dotfiles."
echo "Setup dotfiles with the following command:"
echo "cd src/mine/dotfiles; ./bootstrap.sh"
echo "boxen --env"
read dummy