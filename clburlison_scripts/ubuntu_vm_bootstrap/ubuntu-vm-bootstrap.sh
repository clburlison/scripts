#!/bin/sh

###
# initial updates
###
apt-get update
apt-get -y upgrade
apt-get -y install linux-headers-$(uname -r)

echo "ladmin ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/ers

###
# vmware tools for ubuntu
###
apt-get -y install open-vm-tools-desktop

###
# ssh service
###
apt-get -y install openssh-client
apt-get -y install openssh-server
/etc/init.d/ssh restart

###
# ssh keys for ladmin account
###
mkdir /home/ladmin/.ssh
wget --no-check-certificate \
    'https://cburlison.s3.amazonaws.com/public/public_ssh_keys/birdville_rsa.pub' \
    -O /home/ladmin/.ssh/authorized_keys
chown -R ladmin /home/ladmin/.ssh
chmod -R go-rwsx /home/ladmin/.ssh

###
# clean up
###
apt-get -y autoremove
apt-get -y clean

echo "cleaning up dhcp leases"
rm /var/lib/dhcp/*

echo "cleaning up udev rules"
rm /etc/udev/rules.d/70-persistent-net.rules
mkdir /etc/udev/rules.d/70-persistent-net.rules
rm -rf /dev/.udev/
rm /lib/udev/rules.d/75-persistent-net-generator.rules

###
# zero disk
###
# dd if=/dev/zero of=/EMPTY bs=1M
# rm -f /EMPTY