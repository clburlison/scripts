#!/bin/bash
ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

brew doctor

# Homebrew wants it's path to be first in line so let it
echo export PATH='/usr/local/bin:$PATH' >> ~/.bash_profile

# install mutt
brew install mutt

# setup muttrc file
echo 'I will now setup your ~/.muttrc file'
echo ''
muttrc=~/.muttrc
echo 'set imap_user = "user@localhost"' >>$muttrc
echo 'set imap_pass = "password"' >>$muttrc
echo 'set smtp_url = "smtp://user@smtp.gmail.com:587/"' >>$muttrc
echo 'set smtp_pass = "password"' >>$muttrc
echo 'set from = "user@localhost"' >>$muttrc
echo 'set realname = "I am real"' >>$muttrc
echo 'set folder = "imaps://imap.gmail.com:993"' >>$muttrc
echo 'set spoolfile = "+INBOX"' >>$muttrc
echo 'set postponed = "+[Gmail]/Drafts"' >>$muttrc
echo 'set header_cache = ~/.mutt/cache/headers' >>$muttrc
echo 'set message_cachedir = ~/.mutt/cache/bodies' >>$muttrc
echo 'set certificate_file = ~/.mutt/certificates' >>$muttrc
echo 'set move = no' >>$muttrc
echo 'setup done'

echo "run mutt and accept the ssl certificates"

# this is for reference. how to send an attachment with homebrew.
#         subject       attachment            no message     send to
# mutt -s "test log" -a Desktop/robots.txt < /dev/null -- user@localhost