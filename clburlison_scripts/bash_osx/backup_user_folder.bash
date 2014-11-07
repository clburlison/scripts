#!/bin/sh


rsync -ahx --no-p --no-g --chmod=ugo=rwX --partial-dir=rsync-partial --delete-after --force --times --ignore-errors --timeout=30 --delete-excluded --exclude 'Library' --progress /Volumes/MacintoshHD/Users/USERNAME /Volumes/DATA/


exit 0