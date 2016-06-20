#Clayton's scripts

These are scripts that I have collected from the internet or put together myself.


##What do these files do
Most of these files are pretty self explanatory based off file name or the comments within the script. Most scripts will have header information giving credit/source of the file if not created by me.

_All files provided as is. You run it. You break it. You fix it. I hold no responsibility._

##Makefile
Some directories will have a Makefile for creating packages. I currently am using two types of Makefiles, 'native' and luggage. To verify which Makefile I am using open the file and look for ``include /usr/local/share/luggage/luggage.make`` if that line is present you will need to install [luggage](https://github.com/unixorn/luggage). Other Makefiles would be considered 'native' and use Apple's built in command line tools to create packages.

##Command line tools
Command line tools will need to be installed for some of the items in this repo to work.

```bash
xcode-select --install
```

---
_Shortcuts:_

####Run Power.sh
```bash
curl -fsSL https://raw.githubusercontent.com/clburlison/scripts/master/clburlison_scripts/power_info/power.sh | sh
```