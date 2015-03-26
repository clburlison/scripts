USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make

TITLE=ADacctChange
REVERSE_DOMAIN=com.github.clburlison
PACKAGE_VERSION=1.1
PAYLOAD=\
	pack_script \
	pack-Library-LaunchDaemons-com.github.clburlison.ADacctChange.plist \
	
pack_script: l_Library
	@sudo mkdir -p ${WORK_D}/Library/Scripts
	@sudo ${INSTALL} -m 755 -g wheel -o root ADacctChange.sh ${WORK_D}/Library/Scripts/	