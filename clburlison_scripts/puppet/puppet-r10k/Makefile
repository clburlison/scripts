PKGTITLE=puppet-r10k
PKGVERSION=2.0.3
PKGID=com.github.clburlison.puppet-r10k
# SIGN=--sign "Developer ID Installer: Clayton Burlison"

all: clean build

clean:
	rm -rf pkgroot
	rm -rf out
	rm -rf repo

build: install
	mkdir -p pkgroot/Library/Ruby/Gems/2.0.0
	mkdir -p pkgroot/usr/local/bin
	mkdir -p out
	cp -R repo/* pkgroot/Library/Ruby/Gems/2.0.0/
	cp -R repo/bin/* pkgroot/usr/local/bin
	pkgbuild --root pkgroot --identifier ${PKGID} --version ${PKGVERSION} ${SIGN} --ownership recommended out/${PKGTITLE}-${PKGVERSION}.pkg

install:
	gem install r10k -v ${PKGVERSION} --platform 'Darwin' -i repo -N