USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make

TITLE=LocalAdminMembershipUpdater
REVERSE_DOMAIN=com.github.clburlison
PACKAGE_VERSION=1.3
PAYLOAD=\
	pack_script \
	pack-Library-LaunchDaemons-com.github.clburlison.LocalAdminMembersUpdater.plist \
	
pack_script: l_Library
	@sudo mkdir -p ${WORK_D}/Library/Scripts
	@sudo ${INSTALL} -m 755 -g wheel -o root LocalAdminMembershipUpdater.sh ${WORK_D}/Library/Scripts/	