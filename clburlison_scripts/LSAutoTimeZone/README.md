LSAutoTimeZone
===

This script has a bunch of stolen work from [@arubdesu](https://github.com/arubdesu), [@pudquick](https://github.com/pudquick), and [Munki](https://github.com/munki/munki). It is completely self contained and should do the following:

1. Enable Location Services globally
1. Enable "Set time zone automatically using current location"
1. Force a time zone location lookup at runtime
1. Set correct date, time, and time zone

You can optionally set NTP servers that by changing the `NTP_SERVERS` list and uncommenting `# enable_ntp()` on line 176.

Note: When this code exits, it will generate a warning message - this is to be expected!

    Warning will look like:
    Python[3056:158489] PyObjC: Exception during dealloc of proxy: Cannot remove an observer <TimeZonePref 0x7f846b4b6710>
    for the key path "enabled" from <ATZAdminPrefererences 0x7f846b502a30> because it is not registered as an observer.

The above message can be completely safely ignored.

## Credits
https://gist.github.com/arubdesu/b72585771a9f606ad800
https://gist.github.com/pudquick/ba235b7e90aafb9986158697a457a0d0
https://github.com/munki/munki/blob/master/code/client/munkilib/FoundationPlist.py

I'm 90% sure it will work with 10.8+ however I can't test anything but 10.11 at this time.