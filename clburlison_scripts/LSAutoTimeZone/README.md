LSAutoTimeZone
===

This script has a bunch of stolen work from [@arubdesu](https://github.com/arubdesu), and [@pudquick](https://github.com/pudquick). It is completely self contained and should do the following:

1. Enable Location Services globally
1. Enable "Set time zone automatically using current location"
1. Force a time zone location lookup at runtime
1. Set correct date, time, and time zone

You can optionally set NTP servers that by changing the `NTP_SERVERS` list and uncommenting `# enable_ntp()` on line 234.

## Credits
https://gist.github.com/arubdesu/b72585771a9f606ad800
https://gist.github.com/pudquick/ba235b7e90aafb9986158697a457a0d0
https://gist.github.com/pudquick/c7dd1262bd81a32663f0

Known to work with 10.11 and 10.12 though it should work with 10.8+ (untested).
