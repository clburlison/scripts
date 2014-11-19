#!/bin/sh

source="/Volumes/MacintoshHD/Users/username"
target="/Volumes/FW_Data/"

rsync -ahx --no-p --no-g --chmod=ugo=rwX --partial-dir=rsync-partial --delete-after --force --times --ignore-errors --timeout=30 --delete-excluded --exclude 'Library' --progress ${source} ${target}


exit 0
