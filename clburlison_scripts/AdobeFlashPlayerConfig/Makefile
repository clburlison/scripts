USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make
PB_EXTRA_ARGS+= --sign "Developer ID Installer: Clayton Burlison"

TITLE=AdobeFlashPlayerConfig
REVERSE_DOMAIN=com.github.clburlison
PACKAGE_VERSION=1.0.0
PAYLOAD=\
	pack_config \
	
pack_config: l_Library
	@sudo mkdir -p ${WORK_D}"/Library/Application Support/Macromedia"
	@sudo ${INSTALL} -m 755 -g wheel -o root mms.cfg ${WORK_D}"/Library/Application Support/Macromedia"