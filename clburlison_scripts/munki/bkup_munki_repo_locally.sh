#!/bin/sh
# Resource 1: http://superuser.com/questions/259703/get-mac-tar-to-stop-putting-filenames-in-tar-archives
# Resource 2: http://coolestguidesontheplanet.com/how-to-compress-and-uncompress-files-and-folders-in-os-x-lion-10-7-using-terminal/

# To compress
COPYFILE_DISABLE=1 
tar -zcvf /Volumes/boot/temp/munki_repo_june2015_bkup.tar.gz /Volumes/munki_repo

# To extract
# tar -zxvf archive_name.tar.gz