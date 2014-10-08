#Clayton's scripts

These are scripts that I have collected from the internet or put together myself.


##What do these files do
Most of these files are pretty self explanatory based off file name or the comments within the script.


##Credits
* ``FileVault2Kickoff.sh`` is a script that will check to see if munkireport is installed and running on your Mac. If so and everything is configured correctly this script will then go through the process of enabling FileVault for a single user. This is essentially the same script from [here](https://github.com/munkireport/munkireport-php/blob/master/app/modules/filevault_escrow/script/Sample%20FileVault2%20Kickoff%20Script.sh). Only copied here for easier accessibility. 



####Run boxen-bootstrap.sh
```bash
cd; curl -O https://raw.githubusercontent.com/clburlison/scripts/master/osx/boxen-bootstrap.sh ; chmod 700 boxen-bootstrap.sh; ./boxen-bootstrap.sh
```

####Run FileVault2Kickoff.sh
```bash
cd /tmp/; curl -O https://raw.githubusercontent.com/clburlison/scripts/master/osx/FileVault2Kickoff.sh ; chmod 700 FileVault2Kickoff.sh; ./FileVault2Kickoff.sh
```
