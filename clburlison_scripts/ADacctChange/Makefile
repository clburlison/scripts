USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make

TITLE=ADacctChange
REVERSE_DOMAIN=com.github.clburlison
PACKAGE_VERSION=1.1
PAYLOAD=\
	pack_script \
	pack-BigHonkingText \
	pack-Library-LaunchDaemons-com.github.clburlison.ADacctChange.plist \
	
pack_script: l_Library
	@sudo mkdir -p ${WORK_D}/Library/Scripts
	@sudo ${INSTALL} -m 755 -g wheel -o root ADacctChange.sh ${WORK_D}/Library/Scripts/

pack-BigHonkingText: l_usr
	@sudo mkdir -p ${WORK_D}/usr/local/bin/
	@sudo ${CP} BigHonkingText ${WORK_D}/usr/local/bin/BigHonkingText
	@sudo chown -R root:wheel ${WORK_D}/usr/local/bin/BigHonkingText
	@sudo chmod 744 ${WORK_D}/usr/local/bin/BigHonkingText