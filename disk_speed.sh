#!/bin/sh
sudo dd if=/dev/zero of=/tmp/test bs=1024 count=1048576
wait
exit 0