#Clayton's scripts

These are scripts that I have collected from the internet or put together myself.


##What do these files do
* ``boxen-bootstrap.sh`` is a script that allows me to setup boxen quickly. I am too lazy to remember the commands and use this for setup on VM's. It is quick easy and gets the job done. You will need to modify this if you plan on using.  
* ``FileVault2Kickoff.sh`` is a script that will check to see if munkireport is installed and running on your Mac. If so and everything is configured correctly this script will then go through the process of enabling FileVault for a single user. This is essentially the same script from [here](https://github.com/munkireport/munkireport-php/blob/master/app/modules/filevault_escrow/script/Sample%20FileVault2%20Kickoff%20Script.sh).  
* ``links-to-useful-apps.sh`` Apple likes to hide applications from standard users, which is fine until you need to find them. This script helps me find them by creating alias files to nice locations.  
* ``LogicProX-audio-content.sh`` a bash script that downloads the LogicProX audio content. Need I say more?



####Run boxen-bootstrap.sh
```bash
cd; curl -O https://raw.githubusercontent.com/clburlison/scripts/master/boxen-bootstrap.sh ; chmod 700 boxen-bootstrap.sh; ./boxen-bootstrap.sh
```

####Run FileVault2Kickoff.sh
```bash
cd /tmp/; curl -O https://raw.githubusercontent.com/clburlison/scripts/master/FileVault2Kickoff.sh ; chmod 700 FileVault2Kickoff.sh; ./FileVault2Kickoff.sh
```
