PKGTITLE=r10k_payload
PKGVERSION=1.0.0
PKGID=com.github.clburlison
# SIGN=--sign "Developer ID Installer: Clayton Burlison"

all: clean build

clean:
	rm -rf pkgroot
	rm -rf out

build: install
	mkdir -p pkgroot/Library/Ruby/Gems/2.0.0
	mkdir -p pkgroot/usr/local/bin
	mkdir -p out
	cp -R /Library/Ruby/Gems/2.0.0/* pkgroot/Library/Ruby/Gems/2.0.0/
	# Hacky solution to allow r10k to work on El Cap
	cp -R r10k pkgroot/usr/local/bin
	chmod 755 pkgroot/usr/local/bin/r10k
	pkgbuild --root pkgroot --identifier ${PKGID} --version ${PKGVERSION} ${SIGN} --ownership recommended out/${PKGTITLE}-${PKGVERSION}.pkg

install:
	sudo gem install r10k CFPropertyList sqlite3 hiera-eyaml