Disable Bluetooth Adapter
===

#PLEASE DON'T USE THIS AS IS. I NEVER FINISHED THIS AND SHOULD ONLY BE USED AS A RESOURCE. BLUETOOTH DEVICES WERE ANNOYING BUT I NEVER GOT ALL THE PIECES TOGETHER.


...you know for disabling the bluetooth adapter.


Extra bits that might be of interest to others.



```bash
#delete bluetooth bits from pram
nvram -d bluetoothActiveControllerInfo
nvram -d bluetoothInternalControllerInfo

#remove local user bluetooth stuff
UUID=`ioreg -rd1 -c IOPlatformExpertDevice | awk '/IOPlatformUUID/ { split($0, line, "\""); printf("%s\n", line[4]); }'`
for USER_HOME in /Users/*
do
	USER_UID=`basename "${USER_HOME}"`
	if [ ! "${USER_UID}" = "Shared" ]
	then
    PLIST="${USER_HOME}/Library/Preferences/ByHost/com.apple.Bluetooth.${UUID}"
		if [ -d "${USER_HOME}"/Library/Preferences/ByHost ]
		then
      echo ${PLIST}
      /usr/bin/defaults delete "${USER_HOME}"/Library/Preferences/ByHost/com.apple.Bluetooth.${UUID}
      chown "${USER_UID}" "${USER_HOME}"/Library/Preferences/ByHost
		fi
	fi
done

```